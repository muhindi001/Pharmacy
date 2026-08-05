import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff, Cross } from "lucide-react";
import { login } from "../../api/authApi";

export default function Login() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (event) => {
    event.preventDefault();
    setError("");

    try {
      const response = await login({
        username,
        password,
      });

      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);

      navigate("/dashboard");
    } catch (error) {
      console.log(error.response?.data || error.message);
      setError("Invalid username or password");
    }
  };

  return (
    <div className="min-h-screen bg-slate-400 flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">

        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <div className="bg-blue-900 p-4 rounded-full">
            <Cross className="text-white w-10 h-10" />
          </div>

          <h1 className="mt-4 text-3xl font-bold text-slate-800">
            ABC Pharmacy
          </h1>

          {/* <p className="text-gray-500 mt-1">
            Sign in to your account
          </p> */}
        </div>

        <form onSubmit={handleLogin}>

          {/* Username */}
          <div className="mb-5">
            <label className="block text-sm font-medium mb-2 text-gray-700">
              Username
            </label>

            <input
              type="text"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
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
                value={password}
                onChange={(event) => setPassword(event.target.value)}
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

          {error ? (
            <p className="mt-3 text-sm text-red-600">{error}</p>
          ) : null}

          {/* Change Password */}
          <div className="flex justify-end mt-2">
            <Link
              to="/change-password"
              className="text-bold text-blue-600 hover:text-blue-800 hover:underline"
            >
              Change Password
            </Link>
          </div>

          {/* Login */}
          <button
            type="submit"
            className="mt-6 w-full rounded-lg bg-blue-900 py-3 text-white font-semibold hover:bg-blue-900 transition"
          >
            Login
          </button>

        </form>

      </div>
    </div>
  );
}