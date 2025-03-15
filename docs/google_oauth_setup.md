# Setting Up Google OAuth Authentication

This guide will help you set up Google OAuth for your application.

## 1. Create a Google API Console Project

1. Go to the [Google API Console](https://console.developers.google.com/)
2. Create a new project or select an existing one
3. Click on "Credentials" in the left sidebar
4. Click "Create Credentials" and select "OAuth client ID"
5. If prompted, configure the OAuth consent screen:
   - Select "External" as the user type (unless your app is only for your organization)
   - Enter your app name, user support email, and developer contact information
   - Add the scopes for `email` and `profile`
   - Add your domain to the authorized domains if needed
   - Save and continue

## 2. Create OAuth 2.0 Client ID

1. Select "Web application" as the application type
2. Provide a name for your OAuth 2.0 client
3. Add authorized JavaScript origins:
   - For development: `http://localhost:5000`
   - For production: `https://yourdomain.com`
4. Add authorized redirect URIs:
   - For development: `http://localhost:5000/login/google/authorized`
   - For production: `https://yourdomain.com/login/google/authorized`
5. Click "Create"

## 3. Get Your Client ID and Secret

After creating the client ID, you'll be shown your client ID and client secret. Copy these values.

## 4. Update Your Environment Variables

Update your `.env` file with the client ID and secret:

```
GOOGLE_OAUTH_CLIENT_ID=your-client-id-here
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-here
```

## 5. Restart Your Application

Restart your Flask application to apply the changes.

## Testing the Integration

1. Visit the login page of your application
2. Click "Sign in with Google"
3. Complete the Google authentication process
4. You should be redirected back to your application and logged in

## Troubleshooting

### Common Issues:

1. **Redirect URI mismatch**: Ensure the redirect URI in your Google Console exactly matches the one your application is using.

2. **Missing scopes**: Ensure you've configured the required scopes (`email` and `profile`).

3. **Invalid client secrets**: Double-check your client ID and secret in the `.env` file.

4. **HTTPS requirement in production**: In production, Google requires HTTPS for the redirect URIs.

5. **Consent screen not properly configured**: Ensure your OAuth consent screen is properly configured with the necessary information. 