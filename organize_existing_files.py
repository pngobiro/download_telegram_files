#!/usr/bin/env python3
"""
Organize existing medical files into categories based on medical knowledge.
"""

import os
import shutil
from pathlib import Path

def categorize_file(filename):
    """Categorize a file based on its name using medical knowledge."""
    filename_lower = filename.lower()
    
    # Define comprehensive medical categories with keywords
    categories = {
        '01_Microbiology': [
            'microbiology', 'bacteria', 'virus', 'virology', 'vibrionaceae', 
            'spirillaceae', 'actinomycetaceae', 'spirochaetales', 'escherichia', 
            'klebsiella', 'salmonella', 'proteus', 'brucellaceae', 'neisseria',
            'corynebacteriaceae', 'bacterial', 'pathogen', 'parasitology',
            'herpesviridae', 'hepadnaviridae', 'poxviridae', 'papovaviridae',
            'parpoviridae', 'adenoviridae', 'evasion mechanism', 'malaria',
            'pfalciparum', 'pvivax', 'pmalariae', 'povale'
        ],
        
        '02_Clinical_Chemistry': [
            'clinical chemistry', 'chemistry', 'kidney', 'blood gases', 'liver',
            'lipid profile', 'cardiac markers', 'tumour markers', 'glucose',
            'biochemistry', 'enzymes', 'hormones', 'proteolytic'
        ],
        
        '03_Hematology': [
            'haematology', 'hematology', 'blood', 'anaemia', 'anemia',
            'macrocytic', 'microcytic', 'normocytic', 'hemolytic', 'hemostasis',
            'crossmatch', 'blood group', 'transfusion', 'ahg', 'grouping antisera',
            'phlebotomy', 'coagulation'
        ],
        
        '04_Histopathology_Cytopathology': [
            'histopathology', 'histology', 'cytopathology', 'pap smear', 'pap-smear',
            'museum techniques', 'staining', 'adhesives', 'mounting', 'ringing',
            'histotechniques', 'tissue', 'biopsy', 'cytology'
        ],
        
        '05_Immunology': [
            'immunology', 'immune', 'immunodeficiency', 'hiv', 'sti', 'elisa',
            'flow cytometry', 'antibody', 'antigen', 'serology'
        ],
        
        '06_Emergency_Medical_Services': [
            'ems', 'emergency', 'trauma', 'medical emergencies', 'incident command',
            'ics', 'disaster', 'head injury', 'triage', 'prehospital',
            'special population', 'emergency drugs', 'environmental emergencies'
        ],
        
        '07_Orthopedics_Rehabilitation': [
            'orthopedics', 'orthopaedics', 'fracture', 'dislocation', 'femur',
            'tibia', 'fibula', 'humerus', 'radius', 'shoulder', 'elbow', 'hip',
            'biomechanics', 'traction', 'genu', 'talipes', 'equino-varus',
            'osteomyelitis', 'osteoarthritis', 'osteoporosis', 'rickets',
            'osteomalacia', 'arthritis', 'rheumatoid', 'gouty', 'septic',
            'pyogenic', 'ankylosing spondylitis', 'tumours of bone',
            'rehabilitation', 'physiotherapy', 'exercise therapy', 'electrotherapy',
            'cbr', 'community based rehabilitation'
        ],
        
        '08_Surgery_Perioperative': [
            'surgery', 'perioperative', 'cancer surgery', 'chemotherapy',
            'surgical', 'operative', 'forensic', 'palliative'
        ],
        
        '09_Medicine_Specialty': [
            'medicine', 'paediatrics', 'pediatrics', 'pathology', 'pathophysiology',
            'pharmacology', 'therapeutics', 'psychiatry', 'psychology',
            'dermatology', 'ophthalmology', 'opthalmology', 'e n t', 'ent',
            'genito-urinary', 'grief', 'bereavement', 'end of life'
        ],
        
        '10_Community_Public_Health': [
            'community health', 'public health', 'epidemiology', 'communicable diseases',
            'immunizable', 'childhood immunizable', 'imci', 'i m c i',
            'vector borne', 'ivbd', 'i v b d', 'maternal', 'child health',
            'nutrition', 'primary health care', 'disease prevention',
            'community diagnosis', 'community strategy', 'environment and health',
            'drug and substance abuse', 'occupational health'
        ],
        
        '11_Leadership_Management': [
            'leadership', 'management', 'mngt', 'hsm', 'health service management',
            'human resource', 'delegation', 'decision making', 'theories',
            'principles', 'functions of management', 'conflict management',
            'organization', 'essential medicine', 'commodities', 'supplies',
            'financial resource', 'monitoring', 'evaluation', 'project management',
            'quality assurance', 'resource management'
        ],
        
        '12_Health_Informatics_IT': [
            'health information', 'informatics', 'h i s', 'hospital system',
            'lims', 'computer', 'communication', 'networking', 'data collection',
            'health records', 'health statistics'
        ],
        
        '13_Research_Biostatistics': [
            'research', 'biostatistics', 'statistics', 'sampling', 'sample size',
            'research design', 'problem selection', 'data collection', 'citation',
            'reference', 'measures of relationship', 'data analysis'
        ],
        
        '14_Medical_Imaging': [
            'imaging', 'radiography', 'image processing', 'imaging equipment',
            'imaging therapeutic', 'radiology', 'x-ray'
        ],
        
        '15_Pharmacy': [
            'pharmaceutical', 'pharmacy', 'medicinal chemistry', 'pharmacognosy',
            'phytochemistry', 'physical pharmaceutics', 'pharmaceutical engineering',
            'pharmaceutical jurisprudence', 'pharmaceutical industry'
        ],
        
        '16_Health_Safety_Ethics': [
            'health and safety', 'biosafety', 'safety', 'law', 'ethics',
            'gender', 'law governing', 'kenya biosafety'
        ],
        
        '17_Exams_CATs_FQE': [
            'exam', 'cat', 'fqe', 'question paper', 'mcq', 'revision',
            'past paper', 'test', 'quiz', 'pyq', 'draft'
        ],
        
        '18_Course_Outlines_Notes': [
            'course outline', 'notes', 'lecture', 'unit-', 'unit '
        ]
    }
    
    # Check each category
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return category
    
    # Check file extension for media files
    if filename_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return '19_Images_Photos'
    elif filename_lower.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        return '20_Videos'
    elif filename_lower.endswith(('.pdf', '.PDF')):
        # Try to categorize PDFs more specifically
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in filename_lower:
                    return category
        return '21_PDFs_Uncategorized'
    elif filename_lower.endswith(('.doc', '.docx')):
        return '22_Documents_Uncategorized'
    elif filename_lower.endswith(('.ppt', '.pptx')):
        return '23_Presentations_Uncategorized'
    
    return '99_Uncategorized'

def organize_files(source_dir, target_base_dir, mode='copy'):
    """
    Organize files from source directory into categorized folders.
    
    Args:
        source_dir: Directory containing files to organize
        target_base_dir: Base directory for organized files
        mode: 'copy' or 'move'
    """
    source_path = Path(source_dir)
    target_base_path = Path(target_base_dir)
    
    if not source_path.exists():
        print(f"Error: Source directory '{source_dir}' not found!")
        return
    
    # Create base target directory
    target_base_path.mkdir(parents=True, exist_ok=True)
    
    # Get all files
    all_files = [f for f in source_path.iterdir() if f.is_file()]
    
    print(f"Found {len(all_files)} files to organize...")
    print(f"Mode: {mode.upper()}")
    print("-" * 60)
    
    # Track statistics
    stats = {}
    processed = 0
    
    for file_path in all_files:
        filename = file_path.name
        category = categorize_file(filename)
        
        # Create category directory
        category_dir = target_base_path / category
        category_dir.mkdir(exist_ok=True)
        
        # Determine target path
        target_path = category_dir / filename
        
        # Handle duplicate filenames
        counter = 1
        original_target = target_path
        while target_path.exists():
            stem = original_target.stem
            suffix = original_target.suffix
            target_path = category_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        
        # Copy or move file
        try:
            if mode == 'copy':
                shutil.copy2(file_path, target_path)
            else:
                shutil.move(str(file_path), str(target_path))
            
            processed += 1
            stats[category] = stats.get(category, 0) + 1
            
            if processed % 50 == 0:
                print(f"Processed {processed}/{len(all_files)} files...")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("ORGANIZATION COMPLETE!")
    print("=" * 60)
    print(f"\nTotal files processed: {processed}/{len(all_files)}")
    print(f"\nFiles per category:")
    print("-" * 60)
    
    for category in sorted(stats.keys()):
        count = stats[category]
        print(f"{category:<40} {count:>5} files")
    
    print("\n" + "=" * 60)

def main():
    """Interactive organizer."""
    import sys
    
    # Default paths
    source_dir = "Malcom Skylar/downloads"
    target_dir = "Malcom Skylar/organized"
    
    print("=" * 60)
    print("MEDICAL FILE ORGANIZER")
    print("=" * 60)
    print(f"\nSource: {source_dir}")
    print(f"Target: {target_dir}")
    print("\nThis will organize files into medical categories:")
    print("  - Microbiology, Clinical Chemistry, Hematology")
    print("  - Histopathology, Immunology, EMS")
    print("  - Orthopedics, Surgery, Medicine")
    print("  - Community Health, Leadership, Research")
    print("  - And more...")
    print("\n" + "-" * 60)
    
    # Check if source exists
    if not os.path.exists(source_dir):
        print(f"\nError: Source directory '{source_dir}' not found!")
        return
    
    # Count files
    file_count = len([f for f in os.listdir(source_dir) 
                     if os.path.isfile(os.path.join(source_dir, f))])
    print(f"\nFound {file_count} files to organize")
    
    # Ask for mode
    print("\nChoose organization mode:")
    print("1. COPY files (keeps originals in downloads folder)")
    print("2. MOVE files (removes from downloads folder)")
    
    choice = input("\nEnter your choice (1 or 2) [1]: ").strip() or '1'
    mode = 'copy' if choice == '1' else 'move'
    
    # Confirm
    action_word = "copied" if mode == 'copy' else "moved"
    print(f"\n⚠️  {file_count} files will be {action_word} to '{target_dir}'")
    confirm = input("Continue? (yes/no) [yes]: ").strip().lower() or 'yes'
    
    if confirm not in ['yes', 'y']:
        print("\nOperation cancelled.")
        return
    
    print("\nOrganizing files...\n")
    organize_files(source_dir, target_dir, mode)
    
    print(f"\n✓ Files organized in: {target_dir}")
    print("✓ You can now browse by medical category!")

if __name__ == '__main__':
    main()
