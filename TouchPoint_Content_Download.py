# Query to get all content from Content table
sql = """
SELECT [Name], [Body], [Id], [TypeID]
FROM dbo.Content 
WHERE [Body] IS NOT NULL
ORDER BY [Name]
"""

# Get all content
content_items = q.QuerySql(sql)

# Create a zip file containing all content
import zipfile
import io
import base64

def get_content_type(type_id):
    # Map TypeID to content type
    if type_id == 5:
        return 'Python Scripts'
    elif type_id == 4:
        return 'SQL Scripts'
    elif type_id == 0:
        return 'HTML Content'
    elif type_id == 1:
        return 'Text Content'
    elif type_id == 7:
        return 'Email Templates'
    elif type_id == 3:
        return 'Unknown Emails'
    elif type_id == 6:
        return 'Sent Emails'
    elif type_id == 2:
        return 'Email Templates'
    else:
        return 'Type_%d' % type_id  # Put unknown types in their own folder

# Create a BytesIO object to store the zip file in memory
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    # Track statistics
    stats = {}
    errors = []
    
    # Track filenames to handle duplicates
    used_filenames = {}
    
    for item in content_items:
        if item.Body:  # Only process items that have content
            try:
                # Clean the name to be a valid filename
                clean_name = item.Name.replace('/', '_').replace('\\', '_')
                
                # Get content type from TypeID
                content_type = get_content_type(item.TypeID)
                
                # Initialize stats for this type if not exists
                if content_type not in stats:
                    stats[content_type] = 0
                
                # Add appropriate extension if none exists
                if not clean_name.lower().endswith(('.py', '.sql', '.html', '.htm', '.txt')):
                    if content_type == 'Python Scripts':
                        clean_name += '.py'
                    elif content_type == 'SQL Scripts':
                        clean_name += '.sql'
                    elif content_type in ['HTML Content', 'Email Templates', 'Unknown Emails', 'Sent Emails']:
                        clean_name += '.html'
                    else:
                        clean_name += '.txt'
                
                # Handle duplicate filenames by adding Content ID
                base_name = clean_name
                if clean_name in used_filenames:
                    # Add Content ID to make filename unique
                    name_parts = clean_name.rsplit('.', 1)
                    if len(name_parts) > 1:
                        clean_name = '%s_%s.%s' % (name_parts[0], item.Id, name_parts[1])
                    else:
                        clean_name = '%s_%s' % (clean_name, item.Id)
                used_filenames[base_name] = True
                
                # Create folder structure
                filename = '%s/%s' % (content_type, clean_name)
                
                # Handle Unicode content by encoding to UTF-8
                if isinstance(item.Body, unicode):
                    content = item.Body.encode('utf-8')
                else:
                    content = item.Body
                
                # Add the content to the zip file
                zip_file.writestr(filename, content)
                stats[content_type] += 1
                
            except Exception as e:
                errors.append('Error processing %s: %s' % (item.Name, str(e)))

# Get the zip file content
zip_buffer.seek(0)
zip_content = zip_buffer.getvalue()

# Generate base64 encoded content for download
encoded_content = base64.b64encode(zip_content)

# Create HTML with download button and statistics
print """
<style>
.download-button {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
}
.stats {
    margin: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 4px;
}
.error {
    color: red;
    margin: 10px 0;
}
</style>

<div style='text-align: center; margin: 20px;'>
    <h2>TouchPoint Content Download</h2>
    <div class='stats'>
        <h3>Download Statistics</h3>
"""

# Define the order of content types
content_type_order = [
    'HTML Content',
    'Text Content',
    'SQL Scripts',
    'Python Scripts',
    'Email Templates',
    'Sent Emails',
    'Unknown Emails'
]

# Display stats in the specified order
for content_type in content_type_order:
    if content_type in stats:
        print "<p>%s: %d</p>" % (content_type, stats[content_type])

# Display any remaining types
for content_type, count in sorted(stats.items()):
    if content_type not in content_type_order:
        print "<p>%s: %d</p>" % (content_type, count)

print """
    </div>
    <p>Click the button below to download all content as a zip file.</p>
    <button class='download-button' onclick='downloadContent()'>Download Content</button>
</div>
"""

# Display any errors
if errors:
    print "<div class='error'>"
    print "<h3>Errors Encountered:</h3>"
    for error in errors:
        print "<p>%s</p>" % error
    print "</div>"

print """
<script>
function downloadContent() {
    var content = '%s';
    var link = document.createElement('a');
    link.href = 'data:application/zip;base64,' + content;
    link.download = 'touchpoint_content.zip';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
</script>
""" % encoded_content 