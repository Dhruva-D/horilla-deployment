# Deploying Horilla to Render

This guide will walk you through deploying the Horilla HRMS application to Render.

## Prerequisites

1. A [Render account](https://render.com) (sign up for free)
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Basic knowledge of environment variables

## Deployment Methods

### Method 1: Using render.yaml (Recommended)

This method uses Infrastructure as Code to automatically set up both your web service and database.

1. **Push Your Code to Git**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin master
   ```

2. **Create a New Blueprint in Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your Git repository
   - Render will automatically detect `render.yaml` and create:
     - PostgreSQL database (`horilla-db`)
     - Web service (`horilla`)

3. **Configure Environment Variables**
   
   After the services are created, add these environment variables to your web service:
   
   - `ALLOWED_HOSTS`: Add your Render URL (e.g., `horilla.onrender.com`)
   - `CSRF_TRUSTED_ORIGINS`: Add `https://horilla.onrender.com` (replace with your URL)
   - `TIME_ZONE`: Your timezone (e.g., `America/New_York`, `Europe/London`, `Asia/Kolkata`)
   
   Optional variables:
   - Email settings (if you want email notifications)
   - Cloud storage credentials (for media files)
   - Microsoft Auth credentials (for SSO)

4. **Wait for Deployment**
   - The build process will take 5-10 minutes
   - Monitor the logs in the Render dashboard
   - Once complete, your app will be live!

### Method 2: Manual Setup

If you prefer to set up services manually:

1. **Create PostgreSQL Database**
   - Go to Render Dashboard → "New +" → "PostgreSQL"
   - Name: `horilla-db`
   - Plan: Free or Starter
   - Create Database

2. **Create Web Service**
   - Go to Render Dashboard → "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Name**: `horilla`
     - **Runtime**: Python 3
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn horilla.wsgi:application`
     - **Plan**: Free or Starter

3. **Add Environment Variables**
   
   In your web service settings, add:
   
   | Variable | Value |
   |----------|-------|
   | `PYTHON_VERSION` | `3.10.0` |
   | `DEBUG` | `False` |
   | `SECRET_KEY` | Generate a random string |
   | `DATABASE_URL` | Copy from your database's connection string |
   | `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
   | `CSRF_TRUSTED_ORIGINS` | `https://your-app-name.onrender.com` |
   | `TIME_ZONE` | `UTC` or your timezone |

4. **Deploy**
   - Click "Create Web Service"
   - Wait for the build to complete

## Post-Deployment Steps

### 1. Create Superuser

After successful deployment, you need to create an admin user:

1. Go to your web service in Render Dashboard
2. Click "Shell" tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow the prompts to create your admin account

### 2. Access Your Application

- **Web App**: `https://your-app-name.onrender.com`
- **Admin Panel**: `https://your-app-name.onrender.com/admin`

### 3. Configure Media Files (Optional)

For production, you should use cloud storage for media files:

**Option A: Google Cloud Storage**
1. Create a Google Cloud Storage bucket
2. Add these environment variables:
   - `GS_BUCKET_NAME`
   - `GS_PROJECT_ID`
   - `GOOGLE_APPLICATION_CREDENTIALS`

**Option B: AWS S3**
1. Create an S3 bucket
2. Configure django-storages for S3

## Important Notes

### Free Tier Limitations
- **Web Service**: Spins down after 15 minutes of inactivity (first request may be slow)
- **Database**: 90-day expiration for free PostgreSQL databases
- **Storage**: No persistent disk storage on free tier (use cloud storage)

### Production Recommendations
1. **Upgrade to Paid Plan**: For better performance and no spin-down
2. **Use Cloud Storage**: For media files (uploads, documents, etc.)
3. **Set Up Backups**: Regular database backups
4. **Enable Auto-Deploy**: Automatic deployments on git push
5. **Monitor Logs**: Check logs regularly for errors

## Troubleshooting

### Build Fails

**Issue**: Build command fails
- **Solution**: Check `build.sh` has executable permissions
  ```bash
  chmod +x build.sh
  git add build.sh
  git commit -m "Make build.sh executable"
  git push
  ```

### Database Connection Errors

**Issue**: Can't connect to database
- **Solution**: Verify `DATABASE_URL` is correctly set in environment variables
- Check that the database service is running

### Static Files Not Loading

**Issue**: CSS/JS not loading
- **Solution**: Check that `collectstatic` ran successfully in build logs
- Verify `STATIC_ROOT` and `STATICFILES_STORAGE` in settings.py

### CSRF Errors

**Issue**: CSRF verification failed
- **Solution**: Add your Render URL to `CSRF_TRUSTED_ORIGINS`:
  ```
  CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
  ```

### 502 Bad Gateway

**Issue**: Application won't start
- **Solution**: 
  - Check logs for Python errors
  - Ensure `gunicorn` is in requirements.txt
  - Verify start command is correct

## Updating Your Application

Render automatically deploys when you push to your connected branch:

```bash
git add .
git commit -m "Update application"
git push origin master
```

You can also manually trigger deployments from the Render Dashboard.

## Custom Domain

To use a custom domain:

1. Go to your web service settings
2. Click "Custom Domain"
3. Add your domain
4. Update your DNS records as instructed

## Environment Variables Reference

See `.env.example` for a complete list of available configuration options.

## Support

- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Horilla GitHub](https://github.com/horilla-opensource/horilla)

## Security Checklist

Before going live:

- [ ] Set `DEBUG=False`
- [ ] Use a strong, random `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Set up HTTPS (Render provides this automatically)
- [ ] Enable database backups
- [ ] Set up monitoring and alerts
- [ ] Review and update `CSRF_TRUSTED_ORIGINS`
- [ ] Configure secure email settings if needed

---

**Happy Deploying! 🦍**
