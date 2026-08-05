import React, { useEffect, useState } from "react";
import {
    User,
    Mail,
    Phone,
    Shield,
    Building2,
    Camera,
    Edit,
    KeyRound,
} from "lucide-react";

import { Link } from "react-router-dom";
import { getProfile } from "../../api/authApi";

const loadProfile = async () => {
    const response = await getProfile();
    console.log(response.data);
};
const Profile = () => {

    const [profile, setProfile] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadProfile();
    }, []);

    const loadProfile = async () => {
        try {
            const response = await getProfile();
            setProfile(response.data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen">
                Loading...
            </div>
        );
    }

    return (
        <div className="bg-gray-100 min-h-screen p-6">

            <h1 className="text-3xl font-bold mb-6">
                My Profile
            </h1>

            <div className="bg-white rounded-xl shadow-lg">

                <div className="bg-blue-600 h-32 rounded-t-xl"></div>

                <div className="px-8 pb-8">

                    <div className="flex flex-col md:flex-row justify-between">

                        <div className="flex items-center">

                            <div className="-mt-16 relative">

                                <img
                                    src={
                                        profile.profile_picture ||
                                        "https://via.placeholder.com/150"
                                    }
                                    alt="Profile"
                                    className="w-32 h-32 rounded-full border-4 border-white object-cover"
                                />

                                <button
                                    className="absolute bottom-0 right-0 bg-blue-600 text-white p-2 rounded-full"
                                >
                                    <Camera size={18} />
                                </button>

                            </div>

                            <div className="ml-6 mt-4">

                                <h2 className="text-2xl font-bold">
                                    {profile.full_name}
                                </h2>

                                <p className="text-gray-500">
                                    @{profile.username}
                                </p>

                            </div>

                        </div>

                        <div className="mt-6 md:mt-4 flex gap-3">

                            <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700">

                                <Edit size={18} />

                                Edit Profile

                            </button>

                            <Link
                                to="/change-password"
                                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-700 text-white hover:bg-gray-800"
                            >

                                <KeyRound size={18} />

                                Change Password

                            </Link>

                        </div>

                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-10">

                        <div className="space-y-5">

                            <div className="flex items-center gap-4">

                                <User className="text-blue-600" />

                                <div>

                                    <p className="text-sm text-gray-500">
                                        Full Name
                                    </p>

                                    <p className="font-semibold">
                                        {profile.full_name}
                                    </p>

                                </div>

                            </div>

                            <div className="flex items-center gap-4">

                                <Mail className="text-green-600" />

                                <div>

                                    <p className="text-sm text-gray-500">
                                        Email
                                    </p>

                                    <p className="font-semibold">
                                        {profile.email}
                                    </p>

                                </div>

                            </div>

                            <div className="flex items-center gap-4">

                                <Phone className="text-purple-600" />

                                <div>

                                    <p className="text-sm text-gray-500">
                                        Phone
                                    </p>

                                    <p className="font-semibold">
                                        {profile.phone}
                                    </p>

                                </div>

                            </div>

                        </div>

                        <div className="space-y-5">

                            <div className="flex items-center gap-4">

                                <Shield className="text-red-600" />

                                <div>

                                    <p className="text-sm text-gray-500">
                                        Role
                                    </p>

                                    <p className="font-semibold">
                                        {profile.role}
                                    </p>

                                </div>

                            </div>

                            <div className="flex items-center gap-4">

                                <Building2 className="text-orange-600" />

                                <div>

                                    <p className="text-sm text-gray-500">
                                        Branch
                                    </p>

                                    <p className="font-semibold">
                                        {profile.branch}
                                    </p>

                                </div>

                            </div>

                            <div>

                                <p className="text-sm text-gray-500">
                                    Account Status
                                </p>

                                <span className="inline-block mt-2 px-4 py-1 rounded-full bg-green-100 text-green-700 font-semibold">
                                    {profile.is_active
                                        ? "Active"
                                        : "Inactive"}
                                </span>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </div>
    );
};

export default Profile;