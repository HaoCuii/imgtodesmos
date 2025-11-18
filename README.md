### Frontend
- React with TypeScript
- Vite
- Tailwind CSS
- Axios

### Backend
- Flask
- OpenCV 
- Potrace 
- svgpathtools 

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


