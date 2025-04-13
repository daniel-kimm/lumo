"use client";

import Image from "next/image";
import { useParams, useRouter } from "next/navigation";
import { useState, useEffect } from "react";

export default function MoodboardDetail() {
  const params = useParams();
  const router = useRouter();
  const id = params?.id;
  
  // State for moodboard data
  const [moodboard, setMoodboard] = useState({
    id: 0,
    title: "",
    images: Array(16).fill('/placeholder-image.jpg'),
    colorPalette: ['#A67C52', '#C99C67', '#E6B87A', '#D9BB82', '#A67C52', '#2A3541'],
    styles: ['Cinematic', 'Painterly', 'Illustration'],
    prompt: "A melancholic sci-fi alley in late afternoon light",
    thumbnails: Array(3).fill('/placeholder-image.jpg'),
  });
  
  // Simulating data fetching with useEffect
  useEffect(() => {
    // In a real app, you would fetch data from an API here
    setMoodboard({
      id: Number(id),
      title: "Sci-fi Alleyway",
      images: Array(16).fill('/placeholder-image.jpg'),
      colorPalette: ['#A67C52', '#C99C67', '#E6B87A', '#D9BB82', '#A67C52', '#2A3541'],
      styles: ['Cinematic', 'Painterly', 'Illustration'],
      prompt: "A melancholic sci-fi alley in late afternoon light",
      thumbnails: Array(3).fill('/placeholder-image.jpg'),
    });
  }, [id]);

  return (
    <div style={{ color: 'black', backgroundColor: '#f9f7f4', minHeight: '100vh' }}>
      <style jsx global>{`
        body {
          font-family: 'Poppins', sans-serif;
        }
      `}</style>
      
      {/* Header with darker border */}
      <header className="flex items-center px-8 py-4 border-b border-gray-400">
        <div className="flex items-center gap-8">
          <Image
            src="/lumo-logo.jpg" 
            alt="Lumo logo"
            width={80}
            height={32}
            priority
            unoptimized
          />
          
          <a href="/" className="font-medium" style={{ color: 'black' }}>Home</a>
          <a href="/moodboards" className="font-medium" style={{ color: 'black' }}>Moodboards</a>
        </div>
        
        <div className="flex items-center justify-end gap-4 ml-auto">
          <span className="text-sm text-gray-800">Jane Doe</span>
          <div className="w-10 h-10 bg-[#F0C066] rounded-full"></div>
          <button 
            className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-100 transition-colors"
            onClick={() => alert('Sign out functionality here')}
          >
            Sign Out
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-8 py-10">
        <div className="flex justify-between items-center mb-6">
          <div>
            <button 
              className="text-blue-600 flex items-center gap-1 mb-2 cursor-pointer"
              onClick={() => router.push('/moodboards')}
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
              </svg>
              Back to Moodboards
            </button>
            <h1 className="text-3xl font-bold text-gray-900">
              <span contentEditable suppressContentEditableWarning className="outline-none border-b border-transparent hover:border-gray-300 focus:border-blue-400">
                {moodboard.title}
              </span>
            </h1>
            <p className="text-gray-600 mt-1">Generated from: "{moodboard.prompt}"</p>
          </div>
          
          <div className="flex gap-2">
            <button className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-100 cursor-pointer">
              Export
            </button>
            <button className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-100 cursor-pointer">
              Share
            </button>
          </div>
        </div>
        
        <div className="grid grid-cols-1 gap-10">
          {/* Main images grid - 2 rows of 8 smaller images */}
          <div className="grid grid-cols-4 md:grid-cols-8 gap-2">
            {moodboard.images.map((src, index) => (
              <div 
                key={index} 
                className="aspect-square bg-gray-800 rounded-md overflow-hidden cursor-pointer relative group"
                onClick={() => alert('Image expand functionality here')}
              >
                <Image
                  src={src}
                  alt={`Mood image ${index + 1}`}
                  fill
                  className="object-cover"
                />
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all flex items-center justify-center">
                  <svg 
                    className="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24" 
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
                  </svg>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Color palette, styles, and thumbnails in a 3-column grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-10">
          {/* Color Palette */}
          <div>
            <h3 className="text-xl font-medium mb-4 text-gray-900">Color Palette</h3>
            <div className="flex rounded-md overflow-visible relative mb-8">
              {moodboard.colorPalette.map((color, index) => (
                <div key={index} className="relative flex-1">
                  <div 
                    className="h-12 w-full cursor-pointer group"
                    style={{ backgroundColor: color }}
                  >
                    <div 
                      className="absolute left-1/2 transform -translate-x-1/2 top-14 mt-1 px-2 py-1 bg-gray-900 text-white text-xs rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-20"
                    >
                      {color}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Suggested Styles */}
          <div>
            <h3 className="text-xl font-medium mb-4 text-gray-900">Suggested Styles</h3>
            <div className="flex flex-wrap gap-2">
              {moodboard.styles.map((style, index) => (
                <button 
                  key={index}
                  className="px-4 py-2 bg-gray-200 rounded-full text-sm text-gray-800 cursor-pointer"
                >
                  {style}
                </button>
              ))}
            </div>
          </div>
          
          {/* Thumbnail Ideas */}
          <div>
            <h3 className="text-xl font-medium mb-4 text-gray-900">Thumbnail Ideas</h3>
            <div className="grid grid-cols-3 gap-2">
              {moodboard.thumbnails.map((src, index) => (
                <div 
                  key={index} 
                  className="aspect-square bg-gray-800 rounded-md overflow-hidden cursor-pointer relative"
                >
                  <Image
                    src={src}
                    alt={`Thumbnail idea ${index + 1}`}
                    fill
                    className="object-cover"
                  />
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
} 