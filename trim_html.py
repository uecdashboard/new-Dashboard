import sys

def process(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 0-indexed: line 434 is index 433, line 1047 is index 1046
        # wait, the string we want to remove starts at 433 and ends at 1047 (index 1046, so we slice 1047:)
        top = lines[:433]
        
        # Let's verify we are cutting the right thing
        print(f"Top line: {top[-1].strip()}")
        
        bottom = lines[1047:]
        
        replacement = '''            <div class="review-cards" id="dynamic-gallery-root">
                <div style="text-align:center; padding: 3rem; color: #888;">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">🔄</div>
                    Loading image gallery...
                </div>
            </div>\n'''
        
        new_content = ''.join(top) + replacement + ''.join(bottom)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully pruned {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

process('index.html')
process('dashboard.html')
