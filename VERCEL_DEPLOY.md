# Vercel Deployment Guide

This branch is configured for deployment to Vercel.

## Key Changes Made for Vercel

1. **Removed Docker dependency** - Vercel uses serverless functions instead
2. **Added vercel.json** - Configuration for Vercel deployment
3. **Created api/index.py** - Entry point for Vercel
4. **Updated database configuration** - Uses in-memory SQLite on Vercel (data won't persist)
5. **Added health check endpoint** - For monitoring deployment

## Important Notes

### Database Persistence
⚠️ **Important**: This deployment uses an in-memory SQLite database on Vercel, which means:
- Data will be lost between function invocations
- For production use, you should migrate to a persistent database like:
  - PostgreSQL (recommended with Vercel Postgres)
  - MySQL
  - Any external database service

### Setting up Persistent Database (Recommended)

To use a persistent database, set the `DATABASE_URL` environment variable in Vercel:

```bash
# Example for PostgreSQL
DATABASE_URL=postgresql://username:password@host:port/database
```

## Deployment Steps

1. **Fork/Clone this branch**
2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Select this branch (`vercel-deploy`)

3. **Environment Variables** (Optional but recommended):
   ```
   DATABASE_URL=your_database_url_here
   ```

4. **Deploy**:
   - Vercel will automatically detect the Python project
   - The deployment should complete successfully

## File Uploads

Note that file uploads (images) may not persist on Vercel's serverless environment. For production, consider:
- Using cloud storage (AWS S3, Cloudinary, etc.)
- Updating the image upload functionality accordingly

## Static Files

Static files are served correctly through Vercel's static file handling.

## Local Development

You can still run this locally:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The local version will use the regular SQLite file database. 