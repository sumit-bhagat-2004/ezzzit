"use client";

import { useState } from "react";
import { Menu, X, Zap } from "lucide-react";
import { useUser } from "@auth0/nextjs-auth0";
import Image from "next/image";
import Link from "next/link";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { user } = useUser();

  return (
    <nav className="fixed top-0 w-full z-[100] bg-[#030712] backdrop-blur-xl border-b border-white/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-20 items-center">
          {/* Logo Section */}
          <Link
            href="/"
            className="flex items-center gap-2.5 group cursor-pointer"
          >
            <div className="bg-indigo-600 p-1.5 rounded-lg shadow-[0_0_15px_rgba(79,70,229,0.4)] group-hover:scale-110 transition-transform">
              <Zap size={20} className="text-white fill-white" />
            </div>
            <span className="text-2xl font-bold tracking-tighter text-white">
              ezzzit
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-10">
            <a
              href="#features"
              className="text-sm font-medium text-gray-400 hover:text-white transition-colors"
            >
              Features
            </a>
            <a
              href="#pricing"
              className="text-sm font-medium text-gray-400 hover:text-white transition-colors"
            >
              Pricing
            </a>

            <div className="h-5 w-px bg-white/10 mx-2"></div>

            {user ? (
              <>
                <a
                  href="/auth/logout"
                  className="text-sm font-semibold text-gray-300 hover:text-white transition-colors"
                >
                  Logout
                </a>
                <Image
                  src={user?.picture || "/default-profile.png"}
                  width={32}
                  height={32}
                  className="rounded-full ml-2"
                  alt="User Profile Picture"
                />
              </>
            ) : (
              <a
                href="/auth/login"
                className="relative inline-flex items-center justify-center px-6 py-2.5 text-sm font-bold text-white bg-indigo-600 rounded-full hover:bg-indigo-500 transition-all shadow-[0_0_20px_rgba(79,70,229,0.3)] hover:shadow-indigo-500/50"
              >
                Login
              </a>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 text-gray-400 hover:text-white transition-colors"
            >
              {isOpen ? <X size={28} /> : <Menu size={28} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Overlay */}
      {isOpen && (
        <div className="md:hidden absolute top-20 w-full bg-[#030712] border-b border-white/5 py-8 px-6 space-y-6 shadow-2xl animate-in slide-in-from-top-5">
          <a
            href="#features"
            className="block text-lg font-medium text-gray-300 hover:text-white"
          >
            Features
          </a>
          <a
            href="#pricing"
            className="block text-lg font-medium text-gray-300 hover:text-white"
          >
            Pricing
          </a>
          <div className="pt-6 border-t border-white/5">
            {user ? (
              <a
                href="/auth/logout"
                className="block text-lg font-semibold text-red-400"
              >
                Logout
              </a>
            ) : (
              <a
                href="/auth/login"
                className="block text-center px-4 py-4 text-lg font-bold text-white bg-indigo-600 rounded-2xl shadow-lg"
              >
                Login
              </a>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
