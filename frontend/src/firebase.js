import { initializeApp } from 'firebase/app'
import { 
  getAuth, 
  signInWithPopup, 
  signInWithRedirect,
  getRedirectResult,
  GoogleAuthProvider 
} from 'firebase/auth'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
}

// Initialize Firebase
const app = initializeApp(firebaseConfig)
const auth = getAuth(app)
const provider = new GoogleAuthProvider()
provider.setCustomParameters({
  prompt: 'select_account'
})

// Helper function to handle redirect result
const handleRedirectResult = async () => {
  try {
    const result = await getRedirectResult(auth)
    if (result) {
      return result
    }
    return null
  } catch (error) {
    console.error('Redirect sign-in error:', error)
    throw error
  }
}

// Main sign-in function that tries popup first, then falls back to redirect
const signInWithGoogle = async () => {
  try {
    // First try popup
    const result = await signInWithPopup(auth, provider)
    return result
  } catch (error) {
    // If popup is blocked, try redirect
    if (error.code === 'auth/popup-blocked') {
      console.log('Popup blocked, falling back to redirect method')
      await signInWithRedirect(auth, provider)
      // Return a special flag to indicate redirect is happening
      return { isRedirecting: true }
    }
    throw error
  }
}

export { 
  auth, 
  provider, 
  signInWithGoogle,
  handleRedirectResult,
  signInWithPopup,
  signInWithRedirect,
  getRedirectResult
}