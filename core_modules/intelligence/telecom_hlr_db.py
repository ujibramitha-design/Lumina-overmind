"""
TELEKOMUNIKASI HLR DATABASE
Home Location Register (HLR) Database for Regional Prefix Targeting
Supports HLR_SNIPER mode in mass_scout_advanced.py
"""

# INDONESIA HLR MAPPING DATABASE
# Regional prefix mapping for Telkomsel, Indosat, and XL providers
INDONESIA_HLR_MAPPING = {
    # JABODETABEK (Jakarta, Bogor, Depok, Tangerang, Bekasi)
    'JABODETABEK': {
        'telkomsel': ['08118', '08128', '08129', '08121', '08122', '08123', '08124', '08125', '08126', '08127'],
        'indosat': ['08158', '08159', '08157', '08156', '08155', '08154', '08153', '08152', '08151', '08150'],
        'xl': ['08178', '08179', '08177', '08176', '08175', '08174', '08173', '08172', '08171', '08170'],
        'axis': ['08318', '08319', '08317', '08316', '08315', '08314', '08313', '08312', '08311', '08310'],
        'smartfren': ['08818', '08819', '08817', '08816', '08815', '08814', '08813', '08812', '08811', '08810'],
        'three': ['08958', '08959', '08957', '08956', '08955', '08954', '08953', '08952', '08951', '08950'],
        'all_prefixes': ['08118', '08128', '08129', '08121', '08122', '08123', '08124', '08125', '08126', '08127',
                        '08158', '08159', '08157', '08156', '08155', '08154', '08153', '08152', '08151', '08150',
                        '08178', '08179', '08177', '08176', '08175', '08174', '08173', '08172', '08171', '08170',
                        '08318', '08319', '08317', '08316', '08315', '08314', '08313', '08312', '08311', '08310',
                        '08818', '08819', '08817', '08816', '08815', '08814', '08813', '08812', '08811', '08810',
                        '08958', '08959', '08957', '08956', '08955', '08954', '08953', '08952', '08951', '08950']
    },
    
    # JABAR (Jawa Barat)
    'JABAR': {
        'telkomsel': ['08131', '08132', '08133', '08134', '08135', '08136', '08137', '08138', '08139', '08130'],
        'indosat': ['08160', '08161', '08162', '08163', '08164', '08165', '08166', '08167', '08168', '08169'],
        'xl': ['08180', '08181', '08182', '08183', '08184', '08185', '08186', '08187', '08188', '08189'],
        'axis': ['08320', '08321', '08322', '08323', '08324', '08325', '08326', '08327', '08328', '08329'],
        'smartfren': ['08820', '08821', '08822', '08823', '08824', '08825', '08826', '08827', '08828', '08829'],
        'three': ['08960', '08961', '08962', '08963', '08964', '08965', '08966', '08967', '08968', '08969'],
        'all_prefixes': ['08131', '08132', '08133', '08134', '08135', '08136', '08137', '08138', '08139', '08130',
                        '08160', '08161', '08162', '08163', '08164', '08165', '08166', '08167', '08168', '08169',
                        '08180', '08181', '08182', '08183', '08184', '08185', '08186', '08187', '08188', '08189',
                        '08320', '08321', '08322', '08323', '08324', '08325', '08326', '08327', '08328', '08329',
                        '08820', '08821', '08822', '08823', '08824', '08825', '08826', '08827', '08828', '08829',
                        '08960', '08961', '08962', '08963', '08964', '08965', '08966', '08967', '08968', '08969']
    },
    
    # JATENG (Jawa Tengah)
    'JATENG': {
        'telkomsel': ['08140', '08141', '08142', '08143', '08144', '08145', '08146', '08147', '08148', '08149'],
        'indosat': ['08170', '08171', '08172', '08173', '08174', '08175', '08176', '08177', '08178', '08179'],
        'xl': ['08190', '08191', '08192', '08193', '08194', '08195', '08196', '08197', '08198', '08199'],
        'axis': ['08330', '08331', '08332', '08333', '08334', '08335', '08336', '08337', '08338', '08339'],
        'smartfren': ['08830', '08831', '08832', '08833', '08834', '08835', '08836', '08837', '08838', '08839'],
        'three': ['08970', '08971', '08972', '08973', '08974', '08975', '08976', '08977', '08978', '08979'],
        'all_prefixes': ['08140', '08141', '08142', '08143', '08144', '08145', '08146', '08147', '08148', '08149',
                        '08170', '08171', '08172', '08173', '08174', '08175', '08176', '08177', '08178', '08179',
                        '08190', '08191', '08192', '08193', '08194', '08195', '08196', '08197', '08198', '08199',
                        '08330', '08331', '08332', '08333', '08334', '08335', '08336', '08337', '08338', '08339',
                        '08830', '08831', '08832', '08833', '08834', '08835', '08836', '08837', '08838', '08839',
                        '08970', '08971', '08972', '08973', '08974', '08975', '08976', '08977', '08978', '08979']
    },
    
    # JATIM_BALI (Jawa Timur & Bali)
    'JATIM_BALI': {
        'telkomsel': ['08120', '08121', '08122', '08123', '08124', '08125', '08126', '08127', '08128', '08129'],
        'indosat': ['08150', '08151', '08152', '08153', '08154', '08155', '08156', '08157', '08158', '08159'],
        'xl': ['08160', '08161', '08162', '08163', '08164', '08165', '08166', '08167', '08168', '08169'],
        'axis': ['08340', '08341', '08342', '08343', '08344', '08345', '08346', '08347', '08348', '08349'],
        'smartfren': ['08840', '08841', '08842', '08843', '08844', '08845', '08846', '08847', '08848', '08849'],
        'three': ['08980', '08981', '08982', '08983', '08984', '08985', '08986', '08987', '08988', '08989'],
        'all_prefixes': ['08120', '08121', '08122', '08123', '08124', '08125', '08126', '08127', '08128', '08129',
                        '08150', '08151', '08152', '08153', '08154', '08155', '08156', '08157', '08158', '08159',
                        '08160', '08161', '08162', '08163', '08164', '08165', '08166', '08167', '08168', '08169',
                        '08340', '08341', '08342', '08343', '08344', '08345', '08346', '08347', '08348', '08349',
                        '08840', '08841', '08842', '08843', '08844', '08845', '08846', '08847', '08848', '08849',
                        '08980', '08981', '08982', '08983', '08984', '08985', '08986', '08987', '08988', '08989']
    },
    
    # SUMATERA_UTARA (Sumatera Utara)
    'SUMATERA_UTARA': {
        'telkomsel': ['08110', '08111', '08112', '08113', '08114', '08115', '08116', '08117', '08118', '08119'],
        'indosat': ['08130', '08131', '08132', '08133', '08134', '08135', '08136', '08137', '08138', '08139'],
        'xl': ['08150', '08151', '08152', '08153', '08154', '08155', '08156', '08157', '08158', '08159'],
        'axis': ['08350', '08351', '08352', '08353', '08354', '08355', '08356', '08357', '08358', '08359'],
        'smartfren': ['08850', '08851', '08852', '08853', '08854', '08855', '08856', '08857', '08858', '08859'],
        'three': ['08990', '08991', '08992', '08993', '08994', '08995', '08996', '08997', '08998', '08999'],
        'all_prefixes': ['08110', '08111', '08112', '08113', '08114', '08115', '08116', '08117', '08118', '08119',
                        '08130', '08131', '08132', '08133', '08134', '08135', '08136', '08137', '08138', '08139',
                        '08150', '08151', '08152', '08153', '08154', '08155', '08156', '08157', '08158', '08159',
                        '08350', '08351', '08352', '08353', '08354', '08355', '08356', '08357', '08358', '08359',
                        '08850', '08851', '08852', '08853', '08854', '08855', '08856', '08857', '08858', '08859',
                        '08990', '08991', '08992', '08993', '08994', '08995', '08996', '08997', '08998', '08999']
    },
    
    # SUMATERA_SELATAN (Sumatera Selatan)
    'SUMATERA_SELATAN': {
        'telkomsel': ['08170', '08171', '08172', '08173', '08174', '08175', '08176', '08177', '08178', '08179'],
        'indosat': ['08180', '08181', '08182', '08183', '08184', '08185', '08186', '08187', '08188', '08189'],
        'xl': ['08190', '08191', '08192', '08193', '08194', '08195', '08196', '08197', '08198', '08199'],
        'axis': ['08360', '08361', '08362', '08363', '08364', '08365', '08366', '08367', '08368', '08369'],
        'smartfren': ['08860', '08861', '08862', '08863', '08864', '08865', '08866', '08867', '08868', '08869'],
        'three': ['08900', '08901', '08902', '08903', '08904', '08905', '08906', '08907', '08908', '08909'],
        'all_prefixes': ['08170', '08171', '08172', '08173', '08174', '08175', '08176', '08177', '08178', '08179',
                        '08180', '08181', '08182', '08183', '08184', '08185', '08186', '08187', '08188', '08189',
                        '08190', '08191', '08192', '08193', '08194', '08195', '08196', '08197', '08198', '08199',
                        '08360', '08361', '08362', '08363', '08364', '08365', '08366', '08367', '08368', '08369',
                        '08860', '08861', '08862', '08863', '08864', '08865', '08866', '08867', '08868', '08869',
                        '08900', '08901', '08902', '08903', '08904', '08905', '08906', '08907', '08908', '08909']
    },
    
    # KALIMANTAN
    'KALIMANTAN': {
        'telkomsel': ['08100', '08101', '08102', '08103', '08104', '08105', '08106', '08107', '08108', '08109'],
        'indosat': ['08120', '08121', '08122', '08123', '08124', '08125', '08126', '08127', '08128', '08129'],
        'xl': ['08140', '08141', '08142', '08143', '08144', '08145', '08146', '08147', '08148', '08149'],
        'axis': ['08370', '08371', '08372', '08373', '08374', '08375', '08376', '08377', '08378', '08379'],
        'smartfren': ['08870', '08871', '08872', '08873', '08874', '08875', '08876', '08877', '08878', '08879'],
        'three': ['08910', '08911', '08912', '08913', '08914', '08915', '08916', '08917', '08918', '08919'],
        'all_prefixes': ['08100', '08101', '08102', '08103', '08104', '08105', '08106', '08107', '08108', '08109',
                        '08120', '08121', '08122', '08123', '08124', '08125', '08126', '08127', '08128', '08129',
                        '08140', '08141', '08142', '08143', '08144', '08145', '08146', '08147', '08148', '08149',
                        '08370', '08371', '08372', '08373', '08374', '08375', '08376', '08377', '08378', '08379',
                        '08870', '08871', '08872', '08873', '08874', '08875', '08876', '08877', '08878', '08879',
                        '08910', '08911', '08912', '08913', '08914', '08915', '08916', '08917', '08918', '08919']
    },
    
    # INDOTIM (Indonesia Timur - Sulawesi, Papua, NTT, NTB)
    'INDOTIM': {
        'telkomsel': ['08150', '08151', '08152', '08153', '08154', '08155', '08156', '08157', '08158', '08159'],
        'indosat': ['08160', '08161', '08162', '08163', '08164', '08165', '08166', '08167', '08168', '08169'],
        'xl': ['08170', '08171', '08172', '08173', '08174', '08175', '08176', '08177', '08178', '08179'],
        'axis': ['08380', '08381', '08382', '08383', '08384', '08385', '08386', '08387', '08388', '08389'],
        'smartfren': ['08880', '08881', '08882', '08883', '08884', '08885', '08886', '08887', '08888', '08889'],
        'three': ['08920', '08921', '08922', '08923', '08924', '08925', '08926', '08927', '08928', '08929'],
        'all_prefixes': ['08150', '08151', '08152', '08153', '08154', '08155', '08156', '08157', '08158', '08159',
                        '08160', '08161', '08162', '08163', '08164', '08165', '08166', '08167', '08168', '08169',
                        '08170', '08171', '08172', '08173', '08174', '08175', '08176', '08177', '08178', '08179',
                        '08380', '08381', '08382', '08383', '08384', '08385', '08386', '08387', '08388', '08389',
                        '08880', '08881', '08882', '08883', '08884', '08885', '08886', '08887', '08888', '08889',
                        '08920', '08921', '08922', '08923', '08924', '08925', '08926', '08927', '08928', '08929']
    }
}

# PROVIDER COLOR CODING FOR VISUALIZATION
PROVIDER_COLORS = {
    'telkomsel': '#E3242B',  # Red
    'indosat': '#F5A623',    # Orange
    'xl': '#00A652',        # Green
    'axis': '#3B4992',      # Blue
    'smartfren': '#FF6B35',  # Orange-Red
    'three': '#000000'      # Black
}

# UTILITY FUNCTIONS
def get_region_prefixes(region: str, provider: str = None) -> list:
    """
    Get prefixes for a specific region and optionally filter by provider
    
    Args:
        region (str): Region name (e.g., 'JABODETABEK', 'JABAR')
        provider (str, optional): Provider name to filter by
    
    Returns:
        list: List of prefixes for the region/provider
    """
    if region not in INDONESIA_HLR_MAPPING:
        return []
    
    if provider and provider in INDONESIA_HLR_MAPPING[region]:
        return INDONESIA_HLR_MAPPING[region][provider]
    elif provider:
        # Get prefixes from all regions for specific provider
        all_prefixes = []
        for region_data in INDONESIA_HLR_MAPPING.values():
            if provider in region_data:
                all_prefixes.extend(region_data[provider])
        return list(set(all_prefixes))
    else:
        return INDONESIA_HLR_MAPPING[region]['all_prefixes']

def get_provider_from_prefix(prefix: str) -> str:
    """
    Identify provider from phone prefix
    
    Args:
        prefix (str): 4-5 digit prefix (e.g., '08128')
    
    Returns:
        str: Provider name or 'unknown'
    """
    for region_data in INDONESIA_HLR_MAPPING.values():
        for provider, prefixes in region_data.items():
            if provider != 'all_prefixes' and prefix in prefixes:
                return provider
    return 'unknown'

def get_region_from_prefix(prefix: str) -> str:
    """
    Identify region from phone prefix
    
    Args:
        prefix (str): 4-5 digit prefix (e.g., '08128')
    
    Returns:
        str: Region name or 'unknown'
    """
    for region, region_data in INDONESIA_HLR_MAPPING.items():
        if prefix in region_data['all_prefixes']:
            return region
    return 'unknown'

def format_phone_number(phone: str) -> str:
    """
    Format phone number to standard Indonesian format
    
    Args:
        phone (str): Raw phone number
    
    Returns:
        str: Formatted phone number (e.g., '081281234567')
    """
    import re
    
    # Remove all non-digit characters
    clean_phone = re.sub(r'[^\d]', '', phone)
    
    # Handle different formats
    if clean_phone.startswith('62'):
        return '0' + clean_phone[2:]
    elif clean_phone.startswith('+62'):
        return '0' + clean_phone[3:]
    elif clean_phone.startswith('8'):
        return '0' + clean_phone
    elif clean_phone.startswith('0'):
        return clean_phone
    else:
        return '0' + clean_phone

def validate_indonesian_phone(phone: str) -> bool:
    """
    Validate Indonesian phone number format
    
    Args:
        phone (str): Phone number to validate
    
    Returns:
        bool: True if valid Indonesian phone number
    """
    import re
    
    # Standard Indonesian phone regex
    pattern = r'^(\+62|62|0)8[1-9][0-9]{6,10}$'
    return bool(re.match(pattern, phone))

def extract_prefix_from_phone(phone: str) -> str:
    """
    Extract 4-5 digit prefix from phone number
    
    Args:
        phone (str): Phone number
    
    Returns:
        str: 4-5 digit prefix (e.g., '08128')
    """
    formatted_phone = format_phone_number(phone)
    if len(formatted_phone) >= 5:
        return formatted_phone[:5] if formatted_phone[4] != '0' else formatted_phone[:4]
    return formatted_phone[:4] if len(formatted_phone) >= 4 else ''

# HLR ANALYSIS FUNCTIONS
def analyze_hlr_distribution(region: str) -> dict:
    """
    Analyze HLR prefix distribution for a region
    
    Args:
        region (str): Region name
    
    Returns:
        dict: Distribution analysis by provider
    """
    if region not in INDONESIA_HLR_MAPPING:
        return {}
    
    region_data = INDONESIA_HLR_MAPPING[region]
    analysis = {}
    
    for provider, prefixes in region_data.items():
        if provider != 'all_prefixes':
            analysis[provider] = {
                'prefix_count': len(prefixes),
                'prefixes': prefixes,
                'coverage_percentage': round((len(prefixes) / len(region_data['all_prefixes'])) * 100, 2)
            }
    
    return analysis

def get_regional_coverage_stats() -> dict:
    """
    Get coverage statistics for all regions
    
    Returns:
        dict: Regional coverage statistics
    """
    stats = {}
    
    for region in INDONESIA_HLR_MAPPING.keys():
        all_prefixes = INDONESIA_HLR_MAPPING[region]['all_prefixes']
        stats[region] = {
            'total_prefixes': len(all_prefixes),
            'provider_count': len([p for p in INDONESIA_HLR_MAPPING[region].keys() if p != 'all_prefixes']),
            'coverage_density': len(all_prefixes) / 60  # Assuming 60 prefixes per region max
        }
    
    return stats

# EXPORT FUNCTIONS
def export_hlr_mapping_to_csv(filename: str = 'hlr_mapping.csv'):
    """
    Export HLR mapping to CSV file
    
    Args:
        filename (str): Output filename
    """
    import csv
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Region', 'Provider', 'Prefix'])
        
        for region, region_data in INDONESIA_HLR_MAPPING.items():
            for provider, prefixes in region_data.items():
                if provider != 'all_prefixes':
                    for prefix in prefixes:
                        writer.writerow([region, provider, prefix])

def get_hlr_summary() -> dict:
    """
    Get summary of HLR database
    
    Returns:
        dict: Summary statistics
    """
    total_prefixes = 0
    total_regions = len(INDONESIA_HLR_MAPPING)
    provider_counts = {}
    
    for region_data in INDONESIA_HLR_MAPPING.values():
        for provider, prefixes in region_data.items():
            if provider != 'all_prefixes':
                total_prefixes += len(prefixes)
                provider_counts[provider] = provider_counts.get(provider, 0) + len(prefixes)
    
    return {
        'total_regions': total_regions,
        'total_prefixes': total_prefixes,
        'provider_distribution': provider_counts,
        'average_prefixes_per_region': round(total_prefixes / total_regions, 2)
    }

if __name__ == "__main__":
    # Test functions
    print("=== HLR DATABASE TEST ===")
    print(f"Total regions: {len(INDONESIA_HLR_MAPPING)}")
    
    summary = get_hlr_summary()
    print(f"Total prefixes: {summary['total_prefixes']}")
    
    # Test region lookup
    print(f"\nJABODETABEK prefixes: {len(get_region_prefixes('JABODETABEK'))}")
    print(f"JABAR Telkomsel prefixes: {len(get_region_prefixes('JABAR', 'telkomsel'))}")
    
    # Test prefix analysis
    test_prefix = '08128'
    print(f"\nPrefix {test_prefix}:")
    print(f"  Provider: {get_provider_from_prefix(test_prefix)}")
    print(f"  Region: {get_region_from_prefix(test_prefix)}")
    
    # Test phone formatting
    test_phones = ['+628128123456', '628128123456', '08128123456', '8128123456']
    print(f"\nPhone formatting test:")
    for phone in test_phones:
        formatted = format_phone_number(phone)
        valid = validate_indonesian_phone(formatted)
        print(f"  {phone} -> {formatted} (valid: {valid})")
    
    print(f"\n=== HLR DATABASE SUMMARY ===")
    for key, value in summary.items():
        print(f"{key}: {value}")
