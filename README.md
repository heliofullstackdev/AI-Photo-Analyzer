# AI Photo Analyzer

A simple desktop application that analyzes photos using AI and generates detailed descriptions. Built with Python and Tkinter.

## Features

- **Easy Photo Import**: Import photos from your computer with a simple file dialog
- **AI-Powered Analysis**: Uses OpenAI's GPT-4 Vision API for detailed image analysis
- **Fallback Analysis**: Basic image analysis when API key is not available
- **User-Friendly GUI**: Clean and intuitive interface built with Tkinter
- **Multiple Image Formats**: Supports JPG, PNG, BMP, GIF, TIFF, and more


## Screenshots

The application provides:
- Image preview with automatic resizing
- Detailed AI-generated descriptions
- Status updates and error handling
- Clear and analyze buttons for easy workflow

## Installation

### Prerequisites

- Python 3.7 or higher
- OpenAI API key (optional, for full AI analysis)

### Setup

1. **Clone or download the project files**
   ```bash
   # If you have git
   git clone <your-repo-url>
   cd ai-photo-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key (Optional)**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

## Usage

### Running the Application

```bash
python simple_photo_analyzer.py
```

### How to Use

1. **Launch the application** by running the Python script
2. **Import a photo** by clicking the "Import Photo" button
3. **Select an image file** from your computer
4. **Click "Analyze Photo"** to generate a detailed description
5. **View the results** in the analysis results area

### Without API Key

If you don't have an OpenAI API key, the application will still work but provide basic image information instead of detailed AI analysis:
- Image dimensions
- Color mode
- File format
- File size

### With API Key

With a valid OpenAI API key, you'll get:
- Detailed object recognition
- Scene description
- Color and mood analysis
- Context and setting information
- Comprehensive image understanding

## Project Structure

```
ai-photo-analyzer/
├── simple_photo_analyzer.py # Main GUI application (all-in-one)
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables (your API key)
└── README.md               # This file
```

## Dependencies

- **tkinter**: GUI framework (included with Python)
- **Pillow**: Image processing and display
- **requests**: HTTP requests for API calls
- **python-dotenv**: Environment variable management

## API Information

### OpenAI GPT-4 Vision

The application uses OpenAI's GPT-4 Vision API for image analysis. You'll need:
- An OpenAI account
- API access to GPT-4 Vision
- Credits in your OpenAI account

### Getting an API Key

1. Visit [OpenAI's website](https://openai.com/)
2. Create an account or sign in
3. Go to the API section
4. Generate a new API key
5. Add it to your `.env` file

## Troubleshooting

### Common Issues

1. **"API key not found" error**
   - Make sure you've created a `.env` file
   - Verify your API key is correct
   - Check that the `.env` file is in the same directory as the script

2. **Image won't load**
   - Check that the image file exists
   - Verify the image format is supported
   - Try with a different image file

3. **Analysis fails**
   - Check your internet connection (for API analysis)
   - Verify your OpenAI API key is valid
   - Check your OpenAI account has sufficient credits

### Error Messages

- **File not found**: The selected image file doesn't exist
- **Failed to load image**: The image file is corrupted or in an unsupported format
- **API Error**: There's an issue with the OpenAI API (check your key and credits)

## Customization

### Supported Image Formats

You can modify `config.py` to add more image formats:
```python
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
```

### Analysis Prompt

You can customize the AI analysis prompt in `ai_analyzer.py`:
```python
"text": "Your custom analysis prompt here..."
```

### Window Size

Adjust the application window size in `config.py`:
```python
APP_SIZE = "1000x700"  # Width x Height
```

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section
2. Review the error messages
3. Create an issue in the project repository

