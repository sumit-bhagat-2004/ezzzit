"use client";
import Features from "@/components/Features";
import Hero from "@/components/Hero";
import { useUser } from "@auth0/nextjs-auth0";

export default function Home() {
  const { user, error, isLoading } = useUser();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <Hero />
      <Features />
    </div>
  );
}
