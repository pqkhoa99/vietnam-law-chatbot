#!/bin/bash

# Build script for URA-xLaw Frontend

echo "🏗️  Building URA-xLaw Frontend..."

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build for production
echo "🔧 Building for production..."
npm run build

echo "✅ Build completed! Files are in the 'dist' directory."
echo "🚀 You can now deploy the 'dist' directory to your web server."

# Optional: Preview the build
echo "💡 Run 'npm run preview' to test the production build locally."
