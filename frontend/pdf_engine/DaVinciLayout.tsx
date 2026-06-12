import React, { useState, useEffect, useRef } from 'react';
import { render } from '@react-pdf/renderer';
import { Document, Page, Text, View, Image, StyleSheet, Svg, Rect, Circle, Path, G, Defs, LinearGradient, Stop } from '@react-pdf/renderer';
import { getPalette } from 'node-vibrant';
import { getColor } from 'color-thief';
import puppeteer from 'puppeteer';
import { Browser, Page } from 'puppeteer';

interface DaVinciLayoutProps {
  templateData: {
    title: string;
    subtitle: string;
    content: string;
    images: string[];
    floorplanSvg?: string;
    clientProfile?: {
      name: string;
      preferences: string[];
      budget: string;
      location: string;
    };
    propertyDetails?: {
      type: string;
      size: string;
      bedrooms: number;
      bathrooms: number;
      price: string;
      features: string[];
    };
  };
  outputPath?: string;
  templateType?: 'davinci' | 'modern' | 'classic';
  includeQrCode?: boolean;
  customCss?: string;
}

const DaVinciLayout: React.FC<DaVinciLayoutProps> = ({
  templateData,
  outputPath,
  templateType = 'davinci',
  includeQrCode = true,
  customCss
}) => {
  const [dominantColors, setDominantColors] = useState<string[]>([]);
  const [colorPalette, setColorPalette] = useState<any>(null);
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);
  const [goldenRatio, setGoldenRatio] = useState<number>(1.618);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const browserRef = useRef<Browser | null>(null);

  // Swiss Grid System based on Golden Ratio
  const swissGrid = {
    mainColumns: 12,
    gutters: 20,
    margins: 40,
    baseline: 8,
    goldenRatio: 1.618
  };

  // Calculate column widths based on Golden Ratio
  const calculateColumnWidth = (columns: number) => {
    const totalWidth = 100 - (swissGrid.margins * 2);
    const gutterTotal = (columns - 1) * (swissGrid.gutters / totalWidth * 100);
    const columnWidth = (totalWidth - gutterTotal) / columns;
    return columnWidth;
  };

  // Golden Ratio CSS Grid calculations
  const goldenRatioGrid = {
    display: 'grid',
    gridTemplateColumns: `${goldenRatio}fr 1fr`,
    gap: '2rem',
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '2rem'
  };

  const goldenRatioSections = {
    display: 'grid',
    gridTemplateColumns: '1fr',
    gap: '1.5rem',
    gridTemplateRows: `${goldenRatio}fr 1fr`
  };

  useEffect(() => {
    // Analyze dominant colors from first image
    if (templateData.images.length > 0) {
      analyzeImageColors(templateData.images[0]);
    }
    
    return () => {
      // Cleanup browser instance
      if (browserRef.current) {
        browserRef.current.close();
      }
    };
  }, [templateData.images]);

  const analyzeImageColors = async (imagePath: string) => {
    try {
      // Use node-vibrant for dominant color analysis
      const vibrant = await getPalette(imagePath);
      const palette = vibrant;
      
      setColorPalette(palette);
      
      // Extract dominant colors
      const colors = [
        palette.Vibrant?.hex || '#000000',
        palette.DarkVibrant?.hex || '#000000',
        palette.LightVibrant?.hex || '#FFFFFF',
        palette.Muted?.hex || '#666666',
        palette.DarkMuted?.hex || '#333333'
      ];
      
      setDominantColors(colors);
      
      // Determine if image is dark or light
      const isDark = isColorDark(colors[0]);
      setIsDarkMode(isDark);
      
    } catch (error) {
      console.error('Color analysis failed:', error);
      // Fallback to color-thief
      analyzeWithColorThief(imagePath);
    }
  };

  const analyzeWithColorThief = async (imagePath: string) => {
    try {
      const colorThief = getColor(imagePath);
      const palette = colorThief.getPalette();
      
      if (palette.length > 0) {
        const dominantHex = palette[0];
        setDominantColors([dominantHex]);
        setIsDarkMode(isColorDark(dominantHex));
      }
    } catch (error) {
      console.error('Color-thief analysis failed:', error);
    }
  };

  const isColorDark = (hexColor: string): boolean => {
    // Convert hex to RGB
    const r = parseInt(hexColor.slice(1, 3), 16);
    const g = parseInt(hexColor.slice(3, 5), 16);
    const b = parseInt(hexColor.slice(5, 7), 16);
    
    // Calculate luminance
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    
    return luminance < 0.5;
  };

  const getTypographyClasses = () => {
    if (isDarkMode) {
      return {
        headline: 'font-serif text-4xl md:text-6xl font-bold text-yellow-400 leading-tight',
        subheadline: 'font-serif text-2xl md:text-3xl font-semibold text-yellow-300 leading-snug',
        body: 'font-sans text-base md:text-lg text-gray-200 leading-relaxed',
        accent: 'font-sans text-sm md:text-base text-yellow-500 font-medium',
        caption: 'font-sans text-xs text-gray-400 uppercase tracking-wider'
      };
    } else {
      return {
        headline: 'font-serif text-4xl md:text-6xl font-bold text-gray-900 leading-tight',
        subheadline: 'font-serif text-2xl md:text-3xl font-semibold text-gray-700 leading-snug',
        body: 'font-sans text-base md:text-lg text-gray-600 leading-relaxed',
        accent: 'font-sans text-sm md:text-base text-blue-600 font-medium',
        caption: 'font-sans text-xs text-gray-500 uppercase tracking-wider'
      };
    }
  };

  const getBackgroundClasses = () => {
    if (isDarkMode) {
      return 'bg-gray-900 text-white';
    } else {
      return 'bg-white text-gray-900';
    }
  };

  const typography = getTypographyClasses();
  const backgroundClasses = getBackgroundClasses();

  // PDF Styles for React-PDF
  const pdfStyles = StyleSheet.create({
    page: {
      flexDirection: 'column',
      backgroundColor: isDarkMode ? '#111827' : '#FFFFFF',
      padding: 40,
      fontFamily: 'Helvetica',
    },
    header: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      marginBottom: 30,
      borderBottomWidth: 1,
      borderBottomColor: isDarkMode ? '#374151' : '#E5E7EB',
      borderBottomStyle: 'solid',
      paddingBottom: 20,
    },
    titleSection: {
      flex: 1.618, // Golden Ratio
    },
    imageSection: {
      flex: 1,
      alignItems: 'center',
      justifyContent: 'center',
    },
    mainImage: {
      width: 200,
      height: 200,
      borderRadius: 8,
      objectFit: 'cover',
    },
    title: {
      fontSize: 32,
      fontWeight: 'bold',
      color: isDarkMode ? '#FCD34D' : '#111827',
      marginBottom: 8,
      fontFamily: 'Times-Roman',
    },
    subtitle: {
      fontSize: 18,
      color: isDarkMode ? '#FDE68A' : '#4B5563',
      marginBottom: 16,
      fontFamily: 'Times-Roman',
    },
    content: {
      flexDirection: 'row',
      marginBottom: 30,
    },
    leftColumn: {
      flex: 1.618, // Golden Ratio
      paddingRight: 20,
    },
    rightColumn: {
      flex: 1,
      paddingLeft: 20,
      borderLeftWidth: 1,
      borderLeftColor: isDarkMode ? '#374151' : '#E5E7EB',
      borderLeftStyle: 'solid',
    },
    bodyText: {
      fontSize: 12,
      color: isDarkMode ? '#D1D5DB' : '#4B5563',
      lineHeight: 1.6,
      marginBottom: 16,
    },
    featureBox: {
      backgroundColor: isDarkMode ? '#1F2937' : '#F9FAFB',
      padding: 16,
      borderRadius: 8,
      marginBottom: 16,
      borderWidth: 1,
      borderColor: isDarkMode ? '#374151' : '#E5E7EB',
      borderStyle: 'solid',
    },
    featureTitle: {
      fontSize: 14,
      fontWeight: 'bold',
      color: isDarkMode ? '#FCD34D' : '#111827',
      marginBottom: 8,
    },
    featureText: {
      fontSize: 11,
      color: isDarkMode ? '#9CA3AF' : '#6B7280',
      lineHeight: 1.5,
    },
    floorplanSection: {
      marginTop: 30,
      marginBottom: 30,
    },
    floorplanTitle: {
      fontSize: 16,
      fontWeight: 'bold',
      color: isDarkMode ? '#FCD34D' : '#111827',
      marginBottom: 16,
    },
    svgContainer: {
      width: '100%',
      height: 200,
      backgroundColor: isDarkMode ? '#1F2937' : '#F9FAFB',
      borderRadius: 8,
      borderWidth: 1,
      borderColor: isDarkMode ? '#374151' : '#E5E7EB',
      borderStyle: 'solid',
      padding: 16,
    },
    footer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginTop: 30,
      paddingTop: 20,
      borderTopWidth: 1,
      borderTopColor: isDarkMode ? '#374151' : '#E5E7EB',
      borderTopStyle: 'solid',
    },
    footerText: {
      fontSize: 10,
      color: isDarkMode ? '#6B7280' : '#9CA3AF',
    },
    qrCode: {
      width: 60,
      height: 60,
      backgroundColor: '#FFFFFF',
      padding: 8,
      borderRadius: 4,
    },
  });

  // PDF Document Component
  const PDFDocument = () => (
    <Document>
      <Page size="A4" style={pdfStyles.page}>
        {/* Header Section */}
        <View style={pdfStyles.header}>
          <View style={pdfStyles.titleSection}>
            <Text style={pdfStyles.title}>{templateData.title}</Text>
            <Text style={pdfStyles.subtitle}>{templateData.subtitle}</Text>
          </View>
          <View style={pdfStyles.imageSection}>
            {templateData.images.length > 0 && (
              <Image style={pdfStyles.mainImage} src={templateData.images[0]} />
            )}
          </View>
        </View>

        {/* Main Content */}
        <View style={pdfStyles.content}>
          <View style={pdfStyles.leftColumn}>
            <Text style={pdfStyles.bodyText}>{templateData.content}</Text>
            
            {templateData.propertyDetails && (
              <View style={pdfStyles.featureBox}>
                <Text style={pdfStyles.featureTitle}>Property Details</Text>
                <Text style={pdfStyles.featureText}>
                  Type: {templateData.propertyDetails.type}
                </Text>
                <Text style={pdfStyles.featureText}>
                  Size: {templateData.propertyDetails.size}
                </Text>
                <Text style={pdfStyles.featureText}>
                  Bedrooms: {templateData.propertyDetails.bedrooms}
                </Text>
                <Text style={pdfStyles.featureText}>
                  Bathrooms: {templateData.propertyDetails.bathrooms}
                </Text>
                <Text style={pdfStyles.featureText}>
                  Price: {templateData.propertyDetails.price}
                </Text>
              </View>
            )}
          </View>

          <View style={pdfStyles.rightColumn}>
            {templateData.clientProfile && (
              <View style={pdfStyles.featureBox}>
                <Text style={pdfStyles.featureTitle}>Client Profile</Text>
                <Text style={pdfStyles.featureText}>
                  Name: {templateData.clientProfile.name}
                </Text>
                <Text style={pdfStyles.featureText}>
                  Budget: {templateData.clientProfile.budget}
                </Text>
                <Text style={pdfStyles.featureText}>
                  Location: {templateData.clientProfile.location}
                </Text>
                <Text style={pdfStyles.featureText}>
                  Preferences: {templateData.clientProfile.preferences.join(', ')}
                </Text>
              </View>
            )}

            {templateData.propertyDetails?.features && (
              <View style={pdfStyles.featureBox}>
                <Text style={pdfStyles.featureTitle}>Features</Text>
                {templateData.propertyDetails.features.map((feature, index) => (
                  <Text key={index} style={pdfStyles.featureText}>
                    • {feature}
                  </Text>
                ))}
              </View>
            )}
          </View>
        </View>

        {/* Floorplan Section */}
        {templateData.floorplanSvg && (
          <View style={pdfStyles.floorplanSection}>
            <Text style={pdfStyles.floorplanTitle}>Floor Plan</Text>
            <View style={pdfStyles.svgContainer}>
              <Svg width="100%" height="100%">
                <G dangerouslySetInnerHTML={{ __html: templateData.floorplanSvg }} />
              </Svg>
            </View>
          </View>
        )}

        {/* Footer */}
        <View style={pdfStyles.footer}>
          <Text style={pdfStyles.footerText}>
            Generated by Lumina OS - {new Date().toLocaleDateString()}
          </Text>
          {includeQrCode && (
            <View style={pdfStyles.qrCode}>
              <Text style={pdfStyles.footerText}>QR Code</Text>
            </View>
          )}
        </View>
      </Page>
    </Document>
  );

  // Generate PDF using Puppeteer
  const generatePDF = async (): Promise<string> => {
    try {
      // Launch browser
      if (!browserRef.current) {
        browserRef.current = await puppeteer.launch({
          headless: true,
          args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
      }

      const browser = browserRef.current;
      const page = await browser.newPage();

      // Create HTML content
      const htmlContent = createHTMLContent();

      // Set content and wait for load
      await page.setContent(htmlContent, { waitUntil: 'networkidle0' });

      // Generate PDF
      const pdfBuffer = await page.pdf({
        format: 'A4',
        printBackground: true,
        margin: {
          top: '20mm',
          right: '20mm',
          bottom: '20mm',
          left: '20mm'
        }
      });

      await page.close();

      // Save PDF if output path provided
      if (outputPath) {
        const fs = require('fs');
        fs.writeFileSync(outputPath, pdfBuffer);
        return outputPath;
      }

      // Return base64 encoded PDF
      return pdfBuffer.toString('base64');

    } catch (error) {
      console.error('PDF generation failed:', error);
      throw error;
    }
  };

  // Create HTML content for Puppeteer
  const createHTMLContent = (): string => {
    const css = `
      <style>
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        
        body {
          font-family: 'Times New Roman', serif;
          background-color: ${isDarkMode ? '#111827' : '#FFFFFF'};
          color: ${isDarkMode ? '#D1D5DB' : '#4B5563'};
          line-height: 1.6;
        }
        
        .page {
          width: 210mm;
          min-height: 297mm;
          padding: 20mm;
          display: flex;
          flex-direction: column;
        }
        
        .header {
          display: flex;
          justify-content: space-between;
          margin-bottom: 30px;
          border-bottom: 1px solid ${isDarkMode ? '#374151' : '#E5E7EB'};
          padding-bottom: 20px;
        }
        
        .title-section {
          flex: ${goldenRatio};
        }
        
        .image-section {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .main-image {
          width: 200px;
          height: 200px;
          border-radius: 8px;
          object-fit: cover;
        }
        
        .title {
          font-size: 32px;
          font-weight: bold;
          color: ${isDarkMode ? '#FCD34D' : '#111827'};
          margin-bottom: 8px;
        }
        
        .subtitle {
          font-size: 18px;
          color: ${isDarkMode ? '#FDE68A' : '#4B5563'};
          margin-bottom: 16px;
        }
        
        .content {
          display: flex;
          margin-bottom: 30px;
        }
        
        .left-column {
          flex: ${goldenRatio};
          padding-right: 20px;
        }
        
        .right-column {
          flex: 1;
          padding-left: 20px;
          border-left: 1px solid ${isDarkMode ? '#374151' : '#E5E7EB'};
        }
        
        .body-text {
          font-size: 12px;
          line-height: 1.6;
          margin-bottom: 16px;
        }
        
        .feature-box {
          background-color: ${isDarkMode ? '#1F2937' : '#F9FAFB'};
          padding: 16px;
          border-radius: 8px;
          margin-bottom: 16px;
          border: 1px solid ${isDarkMode ? '#374151' : '#E5E7EB'};
        }
        
        .feature-title {
          font-size: 14px;
          font-weight: bold;
          color: ${isDarkMode ? '#FCD34D' : '#111827'};
          margin-bottom: 8px;
        }
        
        .feature-text {
          font-size: 11px;
          color: ${isDarkMode ? '#9CA3AF' : '#6B7280'};
          line-height: 1.5;
        }
        
        .floorplan-section {
          margin-top: 30px;
          margin-bottom: 30px;
        }
        
        .floorplan-title {
          font-size: 16px;
          font-weight: bold;
          color: ${isDarkMode ? '#FCD34D' : '#111827'};
          margin-bottom: 16px;
        }
        
        .svg-container {
          width: 100%;
          height: 200px;
          background-color: ${isDarkMode ? '#1F2937' : '#F9FAFB'};
          border-radius: 8px;
          border: 1px solid ${isDarkMode ? '#374151' : '#E5E7EB'};
          padding: 16px;
        }
        
        .footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-top: 30px;
          padding-top: 20px;
          border-top: 1px solid ${isDarkMode ? '#374151' : '#E5E7EB'};
        }
        
        .footer-text {
          font-size: 10px;
          color: ${isDarkMode ? '#6B7280' : '#9CA3AF'};
        }
        
        .qr-code {
          width: 60px;
          height: 60px;
          background-color: #FFFFFF;
          padding: 8px;
          border-radius: 4px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 8px;
          color: #000000;
        }
        
        ${customCss || ''}
      </style>
    `;

    const body = `
      <div class="page">
        <div class="header">
          <div class="title-section">
            <h1 class="title">${templateData.title}</h1>
            <p class="subtitle">${templateData.subtitle}</p>
          </div>
          <div class="image-section">
            ${templateData.images.length > 0 ? 
              `<img src="${templateData.images[0]}" class="main-image" alt="${templateData.title}" />` : 
              ''
            }
          </div>
        </div>

        <div class="content">
          <div class="left-column">
            <p class="body-text">${templateData.content}</p>
            
            ${templateData.propertyDetails ? `
              <div class="feature-box">
                <h3 class="feature-title">Property Details</h3>
                <p class="feature-text">Type: ${templateData.propertyDetails.type}</p>
                <p class="feature-text">Size: ${templateData.propertyDetails.size}</p>
                <p class="feature-text">Bedrooms: ${templateData.propertyDetails.bedrooms}</p>
                <p class="feature-text">Bathrooms: ${templateData.propertyDetails.bathrooms}</p>
                <p class="feature-text">Price: ${templateData.propertyDetails.price}</p>
              </div>
            ` : ''}
          </div>

          <div class="right-column">
            ${templateData.clientProfile ? `
              <div class="feature-box">
                <h3 class="feature-title">Client Profile</h3>
                <p class="feature-text">Name: ${templateData.clientProfile.name}</p>
                <p class="feature-text">Budget: ${templateData.clientProfile.budget}</p>
                <p class="feature-text">Location: ${templateData.clientProfile.location}</p>
                <p class="feature-text">Preferences: ${templateData.clientProfile.preferences.join(', ')}</p>
              </div>
            ` : ''}

            ${templateData.propertyDetails?.features ? `
              <div class="feature-box">
                <h3 class="feature-title">Features</h3>
                ${templateData.propertyDetails.features.map(feature => 
                  `<p class="feature-text">• ${feature}</p>`
                ).join('')}
              </div>
            ` : ''}
          </div>
        </div>

        ${templateData.floorplanSvg ? `
          <div class="floorplan-section">
            <h2 class="floorplan-title">Floor Plan</h2>
            <div class="svg-container">
              <svg width="100%" height="100%">
                ${templateData.floorplanSvg}
              </svg>
            </div>
          </div>
        ` : ''}

        <div class="footer">
          <p class="footer-text">
            Generated by Lumina OS - ${new Date().toLocaleDateString()}
          </p>
          ${includeQrCode ? '<div class="qr-code">QR Code</div>' : ''}
        </div>
      </div>
    `;

    return css + body;
  };

  // Manipulate SVG to highlight areas based on client profile
  const manipulateFloorplanSvg = (svgContent: string): string => {
    if (!templateData.clientProfile) return svgContent;

    try {
      // Parse SVG and add highlights based on client preferences
      const parser = new DOMParser();
      const svgDoc = parser.parseFromString(svgContent, 'image/svg+xml');
      const svgElement = svgDoc.documentElement;

      // Add highlight styles
      const style = document.createElement('style');
      style.textContent = `
        .highlight {
          fill: ${dominantColors[0] || '#FCD34D'} !important;
          opacity: 0.3;
        }
        .highlight-stroke {
          stroke: ${dominantColors[0] || '#FCD34D'} !important;
          stroke-width: 3;
          fill: none;
        }
      `;
      svgElement.insertBefore(style, svgElement.firstChild);

      // Highlight areas based on preferences
      templateData.clientProfile.preferences.forEach(preference => {
        const elements = svgElement.querySelectorAll(`[data-area="${preference}"]`);
        elements.forEach(element => {
          element.classList.add('highlight');
        });
      });

      return svgElement.outerHTML;
    } catch (error) {
      console.error('SVG manipulation failed:', error);
      return svgContent;
    }
  };

  return (
    <div className={`min-h-screen ${backgroundClasses}`}>
      {/* Canvas for color analysis */}
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      
      {/* Preview Component */}
      <div style={goldenRatioGrid}>
        <div className="space-y-6">
          <h1 className={typography.headline}>
            {templateData.title}
          </h1>
          <p className={typography.subheadline}>
            {templateData.subtitle}
          </p>
        </div>
        <div className="flex items-center justify-center">
          {templateData.images.length > 0 && (
            <div className="relative w-full h-96 rounded-lg overflow-hidden shadow-2xl">
              <img
                src={templateData.images[0]}
                alt={templateData.title}
                className="object-cover w-full h-full"
                loading="eager"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
            </div>
          )}
        </div>
      </div>

      {/* Color Analysis Display */}
      <div className="mt-8 p-6 rounded-lg border bg-gray-800 border-gray-700">
        <h3 className="text-xl font-bold mb-4 text-yellow-400">Color Analysis</h3>
        <div className="flex space-x-4">
          {dominantColors.map((color, index) => (
            <div key={index} className="flex items-center space-x-2">
              <div 
                className="w-12 h-12 rounded-full border-2 border-gray-300"
                style={{ backgroundColor: color }}
              />
              <span className="text-gray-300 text-sm">{color}</span>
            </div>
          ))}
        </div>
        <div className="mt-4 text-gray-300">
          <p>Mode: {isDarkMode ? 'Dark' : 'Light'}</p>
          <p>Golden Ratio: {goldenRatio}</p>
        </div>
      </div>

      {/* Generate PDF Button */}
      <div className="mt-8 flex justify-center">
        <button
          onClick={generatePDF}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Generate PDF
        </button>
      </div>
    </div>
  );
};

export default DaVinciLayout;
