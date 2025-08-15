# Vercel Deployment Guide for Django BookMyShow Clone

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **PostgreSQL Database**: You'll need a PostgreSQL database (Vercel doesn't support SQLite)
3. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)

## Database Setup

Since Vercel doesn't support SQLite, you need a PostgreSQL database:

### Option 1: Vercel Postgres (Recommended)
1. Go to your Vercel dashboard
2. Create a new Postgres database
3. Copy the connection string

### Option 2: External PostgreSQL
- Use services like:
  - [Supabase](https://supabase.com) (Free tier available)
  - [Neon](https://neon.tech) (Free tier available)
  - [Railway](https://railway.app) (Free tier available)

## Environment Variables

Set these in your Vercel project settings:

```
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.vercel.app
```

## Deployment Steps

1. **Connect Repository**:
   - Go to Vercel dashboard
   - Click "New Project"
   - Import your Git repository

2. **Configure Build Settings**:
   - Framework Preset: Other
   - Build Command: `bash vercel-build`
   - Output Directory: Leave empty
   - Install Command: Leave empty

3. **Set Environment Variables**:
   - Add all required environment variables
   - Make sure `DATABASE_URL` is set

4. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete

## Important Notes

- **Static Files**: Static files are handled by WhiteNoise middleware
- **Media Files**: Media files are served through Vercel's file system
- **Database**: Must use PostgreSQL (SQLite won't work on Vercel)
- **File Uploads**: Limited to 4MB per file on Vercel's free tier

## Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check if all dependencies are in `requirements.txt`
   - Ensure Python version compatibility

2. **Database Connection Error**:
   - Verify `DATABASE_URL` is correct
   - Check if database is accessible from Vercel

3. **Static Files Not Loading**:
   - Ensure `STATIC_ROOT` is properly set
   - Check if `collectstatic` ran successfully

4. **500 Internal Server Error**:
   - Check Vercel function logs
   - Verify environment variables are set

## Post-Deployment

1. **Run Migrations**: They should run automatically during build
2. **Create Superuser**: You may need to create one via Django shell
3. **Test Functionality**: Ensure all features work as expected

## Limitations

- **File Size**: 4MB limit on free tier
- **Execution Time**: 10-second timeout on free tier
- **Memory**: 1024MB RAM limit on free tier
- **Database**: No persistent file storage (use external services)

## Support

If you encounter issues:
1. Check Vercel function logs
2. Verify all environment variables are set
3. Ensure database is accessible
4. Check if all dependencies are compatible
