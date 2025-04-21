# Deploying to Vercel

This guide will help you deploy your Flask AI Video Generator application to Vercel.

## Prerequisites

1. A [Vercel](https://vercel.com) account
2. [Vercel CLI](https://vercel.com/docs/cli) installed on your machine
3. [Git](https://git-scm.com/) for version control

## Step 1: Prepare Your Project

Your project should already be set up with:
- Flask application (`app.py`)
- Required dependencies (`requirements.txt`)
- Vercel configuration (`vercel.json`)

Make sure your project is accessible through a Git repository (GitHub, GitLab, or Bitbucket).

## Step 2: Set Up Environment Variables

1. Create a file called `.env.example` with your required environment variables (but without actual values):
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

2. When you deploy to Vercel, you'll need to add these as environment variables in the Vercel dashboard.

## Step 3: Deploy with Vercel CLI

1. Login to Vercel:
   ```
   vercel login
   ```

2. Deploy the application:
   ```
   vercel
   ```

3. Follow the prompts to connect to your Git repository and configure the project.

4. When asked about environment variables, add your Google API key.

## Step 4: Set Up Environment Variables in Vercel Dashboard

1. Go to the [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to "Settings" > "Environment Variables"
4. Add your environment variables:
   - `GOOGLE_API_KEY`: Your Google Gemini API key

## Step 5: Configure Serverless Functions

Note that the free tier of Vercel has limitations for serverless functions:
- Execution timeout: 10 seconds (may not be enough for video generation)
- Memory: 1GB

For video generation, you may need to:
1. Use a separate server for video processing
2. Use Vercel only for the frontend
3. Consider Vercel Pro for longer execution times

## Important Notes

1. **Storage**: Vercel doesn't provide persistent storage. Your uploaded videos/music and generated content won't persist between function invocations. Consider using cloud storage services like AWS S3 or Google Cloud Storage.

2. **CPU-intensive tasks**: Video generation is CPU-intensive and may not be suitable for serverless environments with time constraints. Consider using a separate server for actual video processing.

3. **Function execution time**: The free tier allows only 10 seconds of execution time, which is not enough for video processing. You'll need Vercel Pro for longer execution times.

## Alternative Approach

For this specific application, a better deployment strategy might be:
1. Host the frontend on Vercel
2. Set up a separate server (e.g., DigitalOcean, AWS EC2) for video processing
3. Use cloud storage for assets and generated videos

This way, you can take advantage of Vercel's fast static hosting while handling the CPU-intensive tasks on a dedicated server. 