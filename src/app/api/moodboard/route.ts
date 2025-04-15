import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const data = await req.json();
    const { prompt } = data;
    
    if (!prompt) {
      return NextResponse.json({ error: 'Prompt is required' }, { status: 400 });
    }
    
    // Call the AWS Lambda function
    const lambdaUrl = process.env.LAMBDA_ENDPOINT || 'https://your-api-gateway-url.amazonaws.com/prod/moodboard';
    
    const response = await fetch(lambdaUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });
    
    if (!response.ok) {
      throw new Error(`Lambda returned status ${response.status}`);
    }
    
    const result = await response.json();
    return NextResponse.json(result);
  } catch (error) {
    console.error('Error generating moodboard:', error);
    return NextResponse.json({ error: 'Failed to generate moodboard' }, { status: 500 });
  }
} 