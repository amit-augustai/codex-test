import { NextRequest, NextResponse } from 'next/server';

export function validateApiKey(request: NextRequest): boolean {
  const apiKey = request.headers.get('x-api-key');
  const expectedKey = process.env.API_SECRET_KEY;

  if (!expectedKey) {
    console.warn('API_SECRET_KEY not configured');
    return false;
  }

  return apiKey === expectedKey;
}

export function unauthorizedResponse(): NextResponse {
  return NextResponse.json(
    { error: 'Unauthorized - Invalid or missing API key' },
    { status: 401 }
  );
}
