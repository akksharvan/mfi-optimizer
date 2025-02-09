import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const backendResponse = await fetch(
      `${process.env.BACKEND_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      }
    )
    
    const data = await backendResponse.json()
    return NextResponse.json(data)
    
  } catch (error) {
    return NextResponse.json(
      { error: 'Prediction service unavailable' },
      { status: 500 }
    )
  }
}