import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

def extract_skills(text):
    """Extract skills section from resume text - works with multiple formats"""
    
    # Try multiple section headers (case-insensitive)
    section_headers = [
        r'Skills?',
        r'Technical Skills?',
        r'Core Competencies',
        r'Key Skills?',
        r'Areas? of Expertise',
        r'Competencies',
        r'Technologies',
        r'Technical Competencies',
        r'Proficiencies',
        r'Technical Expertise'
    ]
    
    # Stop words - section names that indicate end of skills section
    stop_sections = [
        r'Positions? of Responsibility',
        r'Achievements?',
        r'Certifications?',
        r'Awards?',
        r'References?',
        r'Interests?',
        r'Hobbies',
        r'Education',
        r'Work Experience',
        r'Professional Experience'
    ]
    
    skills_text = None
    
    # Try to find the last occurrence of Skills section (more likely to be the actual skills section)
    for header in section_headers:
        pattern = rf'({header})\s*:?\s*(.*?)(?=\n(?:{"|".join(stop_sections)})\s*(?:\n|:)|\Z)'
        matches = list(re.finditer(pattern, text, re.IGNORECASE | re.DOTALL))
        if matches:
            # Use the last match (most likely the actual skills section)
            skills_text = matches[-1].group(2).strip()
            break
    
    if not skills_text:
        # Fallback to pattern-based extraction
        return extract_skills_by_pattern(text)
    
    all_skills = []
    
    # Method 1: Extract from square brackets [skill1, skill2, ...]
    bracket_matches = re.findall(r'\[(.*?)\]', skills_text)
    for bracket_content in bracket_matches:
        items = re.split(r'[,;]', bracket_content)
        for item in items:
            item = item.strip()
            # Filter out URLs and paths
            if item and not item.startswith('/') and not item.startswith('http'):
                all_skills.append(item)
    
    # Method 2: Extract from bullet points and plain text
    lines = skills_text.split('\n')
    for line in lines:
        line = line.strip()
        # Remove bullet points
        line = re.sub(r'^[•◦\-\*➢▪▶]+\s*', '', line)
        
        # Skip if it's a category label (contains colon) but no brackets
        if ':' in line and '[' not in line:
            # Extract skills after the colon
            parts = line.split(':', 1)
            if len(parts) > 1:
                skill_part = parts[1].strip()
                # Split by common delimiters
                items = re.split(r'[,;|]', skill_part)
                for item in items:
                    item = item.strip()
                    if item and len(item.split()) <= 4 and not item.endswith('.'):
                        all_skills.append(item)
        elif line and '[' not in line:
            # Plain text skills (not in brackets, not a category)
            items = re.split(r'[,;|]', line)
            for item in items:
                item = item.strip()
                # Only add if it looks like a skill
                if item and len(item.split()) <= 4 and not item.endswith('.') and ':' not in item:
                    all_skills.append(item)
    
    # Method 3: Extract from pipe-separated format (Python | Java | C++)
    pipe_matches = re.findall(r'([A-Za-z0-9#+\.\s]+(?:\s*\|\s*[A-Za-z0-9#+\.\s]+)+)', skills_text)
    for pipe_content in pipe_matches:
        items = pipe_content.split('|')
        all_skills.extend([item.strip() for item in items if item.strip()])
    
    # Clean and deduplicate
    seen = set()
    unique_skills = []
    
    # Common section names to exclude
    excluded_words = {'projects', 'experience', 'education', 'work', 'responsibilities', 
                     'achievements', 'certifications', 'awards', 'references', 'interests', 
                     'hobbies', 'objective', 'summary', 'profile'}
    
    for skill in all_skills:
        skill = skill.strip()
        skill = re.sub(r'\s+', ' ', skill)  # Normalize whitespace
        skill_lower = skill.lower()
        
        # Filter out unwanted items
        if (skill and 
            skill_lower not in seen and 
            skill_lower not in excluded_words and
            len(skill) >= 1 and 
            not skill.startswith('/') and
            not skill.startswith('http') and
            not any(re.match(header, skill, re.IGNORECASE) for header in section_headers)):
            seen.add(skill_lower)
            unique_skills.append(skill)
    
    return unique_skills if unique_skills else extract_skills_by_pattern(text)

def extract_skills_by_pattern(text):
    """Extract skills using common technology and skill patterns"""
    common_skills = [
        # Programming Languages
        r'Python', r'Java', r'JavaScript', r'C\+\+', r'C#', r'Ruby', r'PHP', r'Swift', r'Kotlin', 
        r'TypeScript', r'Go', r'Rust', r'Scala', r'R\b', r'MATLAB', r'Perl',
        
        # Web Technologies
        r'HTML', r'CSS', r'React', r'Angular', r'Vue\.js', r'Node\.js', r'Django', r'Flask',
        r'Spring', r'Express\.js', r'jQuery', r'Bootstrap', r'Tailwind',
        
        # Databases
        r'MySQL', r'PostgreSQL', r'MongoDB', r'Redis', r'Oracle', r'SQLite', r'SQL Server',
        r'DynamoDB', r'Cassandra', r'Neo4j',
        
        # Cloud & DevOps
        r'AWS', r'Azure', r'Google Cloud', r'GCP', r'Docker', r'Kubernetes', r'Jenkins',
        r'CI/CD', r'GitLab', r'GitHub Actions', r'Terraform', r'Ansible',
        
        # Data Science & ML
        r'Machine Learning', r'Deep Learning', r'TensorFlow', r'PyTorch', r'Scikit-learn',
        r'Pandas', r'NumPy', r'NLP', r'Computer Vision', r'Data Analysis',
        
        # Other Tools
        r'Git', r'Linux', r'REST API', r'GraphQL', r'Microservices', r'Agile', r'Scrum'
    ]
    
    found_skills = []
    for skill_pattern in common_skills:
        matches = re.findall(skill_pattern, text, re.IGNORECASE)
        found_skills.extend(matches)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in found_skills:
        skill_lower = skill.lower()
        if skill_lower not in seen:
            seen.add(skill_lower)
            unique_skills.append(skill)
    
    return unique_skills

resume_path = 'resume.pdf'

# Extract all the text from the pdf 
extracted_text = extract_text_from_pdf(resume_path)

# Extract only skills
skills = extract_skills(extracted_text)

print("=" * 50)
print("EXTRACTED SKILLS:")
print("=" * 50)
if skills:
    for i, skill in enumerate(skills, 1):
        print(f"{i}. {skill}")
else:
    print("No skills found in the resume.")
print("=" * 50)






