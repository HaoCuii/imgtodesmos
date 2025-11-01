# Image to Desmos Converter

A modern web application that converts images into mathematical expressions for Desmos graphing calculator. Built with React, TypeScript, Tailwind CSS, and Flask.

## Features

- **Drag & Drop Image Upload**: Easy-to-use interface for uploading images
- **Edge Detection**: Automatic edge detection using OpenCV
- **SVG Conversion**: Bitmap to vector conversion using Potrace
- **Mathematical Expression Generation**: Converts SVG paths to Desmos-compatible equations
- **Live Preview**: See edge detection results before exporting
- **One-Click Copy**: Copy individual equations or all equations at once
- **Download Support**: Export all equations to a text file
- **Responsive Design**: Beautiful UI built with Tailwind CSS

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Axios (HTTP client)

### Backend
- Flask (Python web framework)
- OpenCV (edge detection)
- Potrace (bitmap to vector conversion)
- svgpathtools (SVG parsing)

## Prerequisites

- Node.js (v16 or higher)
- Python 3.8 to 3.12 (recommended for best compatibility)
  - **Note**: Python 3.13 works but may show NumPy warnings on Windows. These warnings are harmless and won't affect functionality.
- Potrace (for bitmap to SVG conversion)

### Installing Potrace

**Windows:**
```bash
# Using Chocolatey
choco install potrace

# Or download from: http://potrace.sourceforge.net/
```

**macOS:**
```bash
brew install potrace
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install potrace
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Imgtodesmos
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Or use a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Start the Backend Server

```bash
# From the project root
cd backend
python app.py
```

The backend will run on `http://localhost:5000`

### Start the Frontend Development Server

```bash
# In a new terminal, from the project root
cd frontend
npm run dev
```

The frontend will run on `http://localhost:5173` (or another port if 5173 is busy)

### Access the Application

Open your browser and navigate to `http://localhost:5173`

## Usage

1. **Upload an Image**: Click to upload or drag and drop an image file (PNG, JPG, GIF)
2. **Process**: Click the "Process Image" button
3. **View Results**: See the edge detection preview and generated equations
4. **Copy to Desmos**:
   - Click "Copy All" to copy all equations
   - Or click the copy icon next to individual equations
5. **Paste in Desmos**: Visit [Desmos Calculator](https://www.desmos.com/calculator) and paste the equations

## Project Structure

```
Imgtodesmos/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── ImageUploader.tsx
│   │   │   ├── EquationDisplay.tsx
│   │   │   └── ProcessingStatus.tsx
│   │   ├── App.tsx          # Main app component
│   │   └── index.css        # Tailwind imports
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── backend/                  # Flask backend
│   ├── app.py               # Main Flask application
│   ├── requirements.txt     # Python dependencies
│   ├── uploads/             # Uploaded images (auto-created)
│   └── output/              # Processed files (auto-created)
├── assets/                   # Sample images
└── README.md
```

## API Endpoints

### POST `/api/process-image`
Processes an uploaded image and returns Desmos equations.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
  "success": true,
  "equations": ["equation1", "equation2", ...],
  "edgesImage": "data:image/bmp;base64,...",
  "equationCount": 100
}
```

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## How It Works

1. **Image Upload**: User uploads an image through the React frontend
2. **Edge Detection**: Backend uses OpenCV to detect edges in the image
3. **Vectorization**: Potrace converts the bitmap edges to SVG paths
4. **Path Parsing**: svgpathtools parses SVG paths (lines and Bezier curves)
5. **Equation Generation**: Each path is converted to mathematical equations:
   - Lines: `y = mx + b` with domain restrictions
   - Bezier Curves: Parametric equations with `t` parameter
6. **Display**: Frontend displays equations and edge preview
7. **Export**: User can copy equations to paste in Desmos

## Troubleshooting

### Backend won't start
- Make sure all Python dependencies are installed
- Check that Potrace is installed and accessible
- Verify Python version (3.8+)

### Frontend won't start
- Delete `node_modules` and run `npm install` again
- Clear npm cache: `npm cache clean --force`
- Check Node.js version (16+)

### CORS errors
- Make sure the backend is running on port 5000
- Check that flask-cors is installed

### Image processing fails
- Ensure Potrace is properly installed
- Check that the image format is supported
- Verify the uploads/ and output/ directories exist

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your own purposes.

## Original Python Scripts

The original Python scripts that this project is based on can be found in the root directory:
- `edgedetection.py` - Edge detection using OpenCV
- `desmos.py` - SVG to Desmos equation conversion
- `portrace.py` - Potrace integration

## Acknowledgments

- Edge detection powered by [OpenCV](https://opencv.org/)
- Vector conversion by [Potrace](http://potrace.sourceforge.net/)
- UI built with [Tailwind CSS](https://tailwindcss.com/)
- Built with [React](https://react.dev/) and [Vite](https://vitejs.dev/)
