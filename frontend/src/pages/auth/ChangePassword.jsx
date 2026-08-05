import { useState } from "react";
import { Eye, EyeOff, LockKeyhole } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { changePassword } from "../../api/authApi";

export default function ChangePassword() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  });

  const [show, setShow] = useState({
    current: false,
    new: false,
    confirm: false,
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const togglePassword = (field) => {
    setShow({
      ...show,
      [field]: !show[field],
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (form.new_password !== form.confirm_password) {
      alert("New password and confirmation do not match.");
      return;
    }

    // TODO:
    // Call Change Password API

    console.log(form);
  };

  return (
    <div className="min-h-screen bg-slate-400 flex items-center justify-center px-4">

      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">

        <div className="text-center mb-8">

          <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto">

            <LockKeyhole className="text-white w-10 h-10" />

          </div>

          <h2 className="text-3xl font-bold mt-4">
            Change Password
          </h2>

          <p className="text-gray-500 mt-2">
            Update your account password
          </p>

        </div>

        <form onSubmit={handleSubmit} className="space-y-5">

          {/* Current Password */}

          <div>

            <label className="block mb-2 text-sm font-medium">
              Current Password
            </label>

            <div className="relative">

              <input
                type={show.current ? "text" : "password"}
                name="current_password"
                value={form.current_password}
                onChange={handleChange}
                className="w-full border rounded-lg px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Current password"
                required
              />

              <button
                type="button"
                onClick={() => togglePassword("current")}
                className="absolute right-4 top-3.5 text-gray-500"
              >
                {show.current ? (
                  <EyeOff size={20} />
                ) : (
                  <Eye size={20} />
                )}
              </button>

            </div>

          </div>

          {/* New Password */}

          <div>

            <label className="block mb-2 text-sm font-medium">
              New Password
            </label>

            <div className="relative">

              <input
                type={show.new ? "text" : "password"}
                name="new_password"
                value={form.new_password}
                onChange={handleChange}
                className="w-full border rounded-lg px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="New password"
                required
              />

              <button
                type="button"
                onClick={() => togglePassword("new")}
                className="absolute right-4 top-3.5 text-gray-500"
              >
                {show.new ? (
                  <EyeOff size={20} />
                ) : (
                  <Eye size={20} />
                )}
              </button>

            </div>

          </div>

          {/* Confirm Password */}

          <div>

            <label className="block mb-2 text-sm font-medium">
              Confirm Password
            </label>

            <div className="relative">

              <input
                type={show.confirm ? "text" : "password"}
                name="confirm_password"
                value={form.confirm_password}
                onChange={handleChange}
                className="w-full border rounded-lg px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Confirm password"
                required
              />

              <button
                type="button"
                onClick={() => togglePassword("confirm")}
                className="absolute right-4 top-3.5 text-gray-500"
              >
                {show.confirm ? (
                  <EyeOff size={20} />
                ) : (
                  <Eye size={20} />
                )}
              </button>

            </div>

          </div>

          {/* Buttons */}

          <div className="flex gap-3 pt-2">

            <button
              type="button"
              onClick={() => navigate("/")}
              className="w-1/2 border border-gray-300 rounded-lg py-3 font-semibold hover:bg-gray-100"
            >
              Cancel
            </button>

            <button
              type="submit"
              className="w-1/2 bg-blue-600 text-white rounded-lg py-3 font-semibold hover:bg-blue-700"
            >
              Change Password
            </button>

          </div>

        </form>

      </div>

    </div>
  );
}