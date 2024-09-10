import Link from 'next/link';
import { Home, User } from 'lucide-react';
import { Button } from "@/components/ui/button";
import SignIn from '@/components/signin';

const NavBar = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <span className="text-2xl font-bold text-red-600">A+I</span>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link href="/" className="inline-flex items-center px-1 pt-1 text-sm font-medium">
                <Button variant="ghost">
                  <Home className="mr-2 h-4 w-4" />
                  Home
                </Button>
              </Link>
              <Link href="/dashboard" className="inline-flex items-center px-1 pt-1 text-sm font-medium">
                <Button variant="ghost">
                  <User className="mr-2 h-4 w-4" />
                  Professor Dashboard
                </Button>
              </Link>
            </div>
          </div>
          <div className="hidden sm:ml-6 sm:flex sm:items-center">
            <SignIn />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;