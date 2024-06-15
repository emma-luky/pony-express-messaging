import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route, Link } from 'react-router-dom';
import { AuthProvider } from "./context/auth";
import { UserProvider } from "./context/user";
import { useAuth } from "./hooks";
import Chats from './components/Chats';
import Login from './components/Login';
import Registration from './components/Registration';
import TopNav from './components/TopNav';
import Profile from './components/Profile';

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function Home() {
  const { isLoggedIn, logout } = useAuth();

  return (
    <div className="mx-auto text-center px-4 py-8">
      <h2 className="text-2xl">Welcome to Pony Express</h2>
      <p className="py-2">An instant messaging web application</p>
      <Link className="hover:bg-violet-600" to="/login">Get Started!</Link>
    </div>
  );
}

function Header() {
  return (
    <header>
      <TopNav />
    </header>
  );
}

function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Chats />} />
      <Route path="/chats" element={<Chats />} />
      <Route path="/chats/:chatID" element={<Chats />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/error/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/error/404" />} />
    </Routes>
  );
}

function UnauthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/registration" element={<Registration />} />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

function Main() {
  const { isLoggedIn } = useAuth();
  return (
    <main className="max-h-main">
      {isLoggedIn ?
        <AuthenticatedRoutes /> :
        <UnauthenticatedRoutes />
      }
    </main>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <UserProvider>
            <Header />
            <Main />
          </UserProvider>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App
