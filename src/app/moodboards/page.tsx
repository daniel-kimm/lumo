"use client";

import Image from "next/image";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Moodboards() {
  const router = useRouter();
  
  // Sample moodboard data - in a real app this would come from an API
  const [moodboards] = useState([
    { id: 1, title: "Sci-fi Alleyway", thumbnail: "/placeholder-image.jpg", created: "2 days ago" },
    { id: 2, title: "Cyberpunk Interior", thumbnail: "/placeholder-image.jpg", created: "1 week ago" },
    { id: 3, title: "Cozy Cottage", thumbnail: "/placeholder-image.jpg", created: "2 weeks ago" },
    { id: 4, title: "Desert Landscape", thumbnail: "/placeholder-image.jpg", created: "3 weeks ago" },
    { id: 5, title: "Futuristic City", thumbnail: "/placeholder-image.jpg", created: "1 month ago" },
    { id: 6, title: "Ocean Sunset", thumbnail: "/placeholder-image.jpg", created: "1 month ago" },
  ]);

  const navigateToMoodboard = (id: number) => {
    router.push(`/moodboards/${id}`);
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
        <div className="flex justify-between items-center mb-10">
          <h1 className="text-3xl font-bold text-gray-900">Your Moodboards</h1>
          <button 
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors cursor-pointer"
            onClick={() => router.push('/')}
          >
            Create New
          </button>
        </div>

        {/* Moodboard grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {moodboards.map((moodboard) => (
            <div 
              key={moodboard.id}
              className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow cursor-pointer"
              onClick={() => navigateToMoodboard(moodboard.id)}
            >
              <div className="aspect-video relative bg-gray-100">
                <Image
                  src={moodboard.thumbnail}
                  alt={moodboard.title}
                  fill
                  className="object-cover"
                />
              </div>
              <div className="p-4">
                <h3 className="text-xl font-medium text-gray-900">{moodboard.title}</h3>
                <p className="text-sm text-gray-500 mt-1">Created {moodboard.created}</p>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
} 