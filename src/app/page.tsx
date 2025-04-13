"use client";

import Image from "next/image";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  // State to track if a prompt has been entered
  const [prompt, setPrompt] = useState("");
  const [showMoodboard, setShowMoodboard] = useState(false);
  
  // Sample data for mood board images
  const moodboardImages = Array(16).fill('/placeholder-image.jpg');
  // Sample color palette
  const colorPalette = ['#A67C52', '#C99C67', '#E6B87A', '#D9BB82', '#A67C52', '#2A3541'];
  // Sample suggested styles
  const suggestedStyles = ['Cinematic', 'Painterly', 'Illustration'];

  // Handle prompt submission
  const handleSubmitPrompt = () => {
    if (prompt.trim()) {
      setShowMoodboard(true);
    }
  };

  // Clear prompt and reset view
  const handleClearPrompt = () => {
    setPrompt("");
    setShowMoodboard(false);
  };

  // Save the current moodboard
  const handleSaveMoodboard = () => {
    // In a real app, this would save to a database
    alert("Moodboard saved!");
    // Optionally navigate to the moodboards page
    // router.push('/moodboards');
  };

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
            className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-100 transition-colors cursor-pointer"
            onClick={() => alert('Sign out functionality here')}
          >
            Sign Out
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-8 py-10">
        {!showMoodboard ? (
          // Center the prompt input when no moodboard is showing
          <div className="flex flex-col items-center justify-center" style={{ minHeight: "70vh" }}>
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Hello, Jane Doe</h1>
            <div className="relative w-full max-w-4xl">
              <input
                type="text"
                placeholder="Give me a moodboard for a melancholic sci-fi alley in late afternoon light"
                className="w-full p-4 pr-12 rounded-full border border-gray-300 bg-white text-gray-800 placeholder-gray-500"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSubmitPrompt()}
              />
              <button 
                className="absolute right-4 top-1/2 -translate-y-1/2 text-blue-600 cursor-pointer"
                onClick={handleSubmitPrompt}
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </button>
            </div>
          </div>
        ) : (
          // Regular layout when moodboard is showing
          <>
            <div className="relative mb-12 flex items-center">
              <input
                type="text"
                placeholder="Give me a moodboard for a melancholic sci-fi alley in late afternoon light"
                className="w-full p-4 pr-24 rounded-full border border-gray-300 bg-white text-gray-800 placeholder-gray-500"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSubmitPrompt()}
              />
              <div className="absolute right-4 flex gap-2">
                <button 
                  className="text-gray-500 hover:text-gray-700 cursor-pointer"
                  onClick={handleClearPrompt}
                  title="Clear prompt"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
                <button 
                  className="text-blue-600 cursor-pointer"
                  onClick={handleSubmitPrompt}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                  </svg>
                </button>
              </div>
            </div>
            
            <div className="grid grid-cols-1 gap-10">
              <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold text-gray-900">Moodboard</h2>
                <button 
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors cursor-pointer"
                  onClick={handleSaveMoodboard}
                >
                  Save to Moodboards
                </button>
              </div>
              
              <div className="grid grid-cols-4 md:grid-cols-8 gap-2">
                {moodboardImages.map((src, index) => (
                  <div 
                    key={index} 
                    className="aspect-square bg-gray-800 rounded-md overflow-hidden cursor-pointer relative group"
                    onClick={() => alert('Image expand functionality here')}
                  >
                    <Image
                      src={src}
                      alt={`Mood image ${index + 1}`}
                      width={100}
                      height={100}
                      className="w-full h-full object-cover"
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
            
            {/* Sidebar content */}
            <div className="grid grid-cols-3 gap-8 mt-10">
              {/* Color Palette */}
              <div>
                <h3 className="text-2xl font-medium mb-4 text-gray-900">Color Palette</h3>
                <div className="flex rounded-md overflow-visible relative mb-8">
                  {colorPalette.map((color, index) => (
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
                <h3 className="text-2xl font-medium mb-4 text-gray-900">Suggested Styles</h3>
                <div className="flex flex-wrap gap-2">
                  {suggestedStyles.map((style, index) => (
                    <button 
                      key={index}
                      className="px-4 py-2 bg-gray-200 rounded-full text-sm text-gray-800 cursor-pointer"
                    >
                      {style}
                    </button>
                  ))}
                </div>
              </div>
              
              {/* Thumbnails */}
              <div>
                <h3 className="text-2xl font-medium mb-4 text-gray-900">Thumbnails</h3>
                <div className="grid grid-cols-3 gap-2">
                  {Array(3).fill('/placeholder-image.jpg').map((src, index) => (
                    <div 
                      key={index} 
                      className="aspect-square bg-gray-800 rounded-md overflow-hidden cursor-pointer relative group"
                      onClick={() => alert('Thumbnail expand functionality here')}
                    >
                      <Image
                        src={src}
                        alt={`Thumbnail ${index + 1}`}
                        width={100}
                        height={100}
                        className="w-full h-full object-cover"
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
            </div>
          </>
        )}
      </main>
    </div>
  );
}