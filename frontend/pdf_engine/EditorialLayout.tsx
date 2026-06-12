import React, { useState, useEffect } from 'react';
import { getDominantColor } from 'node-vibrant';
import { getColor } from 'color-thief';
import Image from 'next/image';

interface EditorialLayoutProps {
  images: string[];
  title: string;
  subtitle: string;
  content: string;
}

const EditorialLayout: React.FC<EditorialLayoutProps> = ({
  images,
  title,
  subtitle,
  content
}) => {
  const [dominantColor, setDominantColor] = useState<string>('#000000');
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);
  const [goldenRatio, setGoldenRatio] = useState<number>(1.618);
  
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
    // Analyze dominant color from first image
    if (images.length > 0) {
      analyzeImageColors(images[0]);
    }
  }, [images]);
  
  const analyzeImageColors = async (imagePath: string) => {
    try {
      // Use node-vibrant for dominant color analysis
      const vibrant = await getDominantColor(imagePath);
      const hexColor = vibrant.hex;
      
      setDominantColor(hexColor);
      
      // Determine if image is dark or light
      const isDark = isColorDark(hexColor);
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
        setDominantColor(dominantHex);
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
        accent: 'font-sans text-sm md:text-base text-yellow-500 font-medium'
      };
    } else {
      return {
        headline: 'font-serif text-4xl md:text-6xl font-bold text-gray-900 leading-tight',
        subheadline: 'font-serif text-2xl md:text-3xl font-semibold text-gray-700 leading-snug',
        body: 'font-sans text-base md:text-lg text-gray-600 leading-relaxed',
        accent: 'font-sans text-sm md:text-base text-blue-600 font-medium'
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
  
  return (
    <div className={`min-h-screen ${backgroundClasses}`}>
      {/* Header Section */}
      <header className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-transparent to-black/20" />
        <div style={goldenRatioGrid}>
          <div className="space-y-6">
            <h1 className={typography.headline}>
              {title}
            </h1>
            <p className={typography.subheadline}>
              {subtitle}
            </p>
          </div>
          <div className="flex items-center justify-center">
            <div className="relative w-full h-96 rounded-lg overflow-hidden shadow-2xl">
              <Image
                src={images[0]}
                alt={title}
                fill
                className="object-cover"
                priority
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
            </div>
          </div>
        </div>
      </header>
      
      {/* Content Section */}
      <main className={backgroundClasses}>
        <div style={goldenRatioSections}>
          {/* Main Content */}
          <div className="space-y-6">
            <div className="prose prose prose-lg max-w-none">
              <p className={typography.body}>
                {content}
              </p>
            </div>
            
            {/* Additional Images */}
            {images.slice(1).map((image, index) => (
              <div key={index} className="relative rounded-lg overflow-hidden shadow-xl">
                <Image
                  src={image}
                  alt={`${title} - Image ${index + 1}`}
                  width={800}
                  height={600}
                  className="object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />
              </div>
            ))}
          </div>
          
          {/* Sidebar */}
          <div className="space-y-6">
            <div className={`p-6 rounded-lg border ${isDarkMode ? 'border-gray-700 bg-gray-800' : 'border-gray-200 bg-white'}`}>
              <h3 className={`text-xl font-bold mb-4 ${isDarkMode ? 'text-yellow-400' : 'text-gray-900'}`}>
                Color Analysis
              </h3>
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <div 
                    className="w-12 h-12 rounded-full border-2 border-gray-300"
                    style={{ backgroundColor: dominantColor }}
                  />
                  <div>
                    <p className={`font-medium ${isDarkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                      Dominant Color
                    </p>
                    <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                      {dominantColor}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <div className={`w-4 h-4 rounded-full ${isDarkMode ? 'bg-yellow-400' : 'bg-blue-600'}`} />
                  <p className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                    {isDarkMode ? 'Dark Mode' : 'Light Mode'} Active
                  </p>
                </div>
              </div>
            </div>
            
            <div className={`p-6 rounded-lg border ${isDarkMode ? 'border-gray-700 bg-gray-800' : 'border-gray-200 bg-white'}`}>
              <h3 className={`text-xl font-bold mb-4 ${isDarkMode ? 'text-yellow-400' : 'text-gray-900'}`}>
                Golden Ratio Layout
              </h3>
              <div className="space-y-2">
                <p className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                  Aspect Ratio: {goldenRatio}
                </p>
                <p className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                  Grid System: CSS Grid
                </p>
                <p className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                  Typography: Serif + Sans-serif
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className={`border-t ${isDarkMode ? 'border-gray-700 bg-gray-800' : 'border-gray-200 bg-white'}`}>
        <div className="max-w-7xl mx-auto px-4 py-8">
          <p className={`text-center ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            Editorial Design by Senior Art Director
          </p>
        </div>
      </footer>
    </div>
  );
};

export default EditorialLayout;
