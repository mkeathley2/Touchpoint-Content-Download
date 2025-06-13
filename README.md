# TouchPoint Content Download

A Python script for TouchPoint Church Management System that downloads and organizes all content from your TouchPoint database into a structured zip file.

## Features

- Downloads all content from your TouchPoint Content table
- Organizes files by type:
  - HTML Content
  - Text Content
  - SQL Scripts
  - Python Scripts
  - Email Templates
  - Sent Emails
  - Unknown Emails
- Automatically adds appropriate file extensions
- Handles duplicate filenames
- Provides download statistics
- Creates a downloadable zip file

## Requirements

- Python 2.7
- TouchPoint Church Management System
- Access to TouchPoint database

## Usage

1. Place the script in your TouchPoint Python Reports directory
2. Run the script through TouchPoint's Python Reports interface
3. Click the "Download Content" button to get your zip file

## File Organization

The script creates a zip file with the following structure:
```
touchpoint_content.zip
├── HTML Content/
├── Text Content/
├── SQL Scripts/
├── Python Scripts/
├── Email Templates/
├── Sent Emails/
└── Unknown Emails/
```

## Notes

- Files are organized based on their TypeID in the TouchPoint Content table
- Duplicate filenames are handled by appending the Content ID
- All files are properly encoded to handle special characters
- The script provides statistics about the number of files in each category

## License

This project is licensed under the MIT License - see the LICENSE file for details. 