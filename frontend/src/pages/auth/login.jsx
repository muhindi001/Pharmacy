import { useState } from "react";
import { Link } from "react-router-dom";
import { Eye, EyeOff, Cross } from "lucide-react";

export default function Login() {
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    // TODO:
    // Call login API here
  };

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">

        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <div className="bg-blue-600 p-4 rounded-full">
            <Cross className="text-white w-10 h-10" />
          </div>

          <h1 className="mt-4 text-3xl font-bold text-slate-800">
            ABC Pharmacy
          </h1>

          <p className="text-gray-500 mt-1">
            Sign in to your account
          </p>
        </div>

        <form onSubmit={handleSubmit}>

          {/* Username */}
          <div className="mb-5">
            <label className="block text-sm font-medium mb-2 text-gray-700">
              Username
            </label>

            <input
              type="text"
              placeholder="Enter username"
              className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-700">
              Password
            </label>

            <div className="relative">

              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter password"
                className="w-full rounded-lg border border-gray-300 px-4 py-3 pr-12 outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />

              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-3.5 text-gray-500"
              >
                {showPassword ? (
                  <EyeOff size={20} />
                ) : (
                  <Eye size={20} />
                )}
              </button>

            </div>
          </div>

          {/* Change Password */}
          <div className="flex justify-end mt-2">
            <Link
              to="/change-password"
              className="text-sm text-blue-600 hover:text-blue-800 hover:underline"
            >
              Change Password
            </Link>
          </div>

          {/* Login */}
          <button
            type="submit"
            className="mt-6 w-full rounded-lg bg-blue-800 py-3 text-white font-semibold hover:bg-blue-900 transition"
          >
            Login
          </button>

        </form>

      </div>
    </div>
  );
}