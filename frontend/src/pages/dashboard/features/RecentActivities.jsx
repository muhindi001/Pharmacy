import React from "react";

const RecentActivities = ({ activities = [] }) => {

    return (

        <div className="bg-white rounded-xl shadow p-5">

            <h2 className="text-lg font-semibold mb-5">

                Recent Activities

            </h2>

            <div className="space-y-4">

                {activities.length === 0 ? (

                    <p className="text-gray-500">

                        No recent activity.

                    </p>

                ) : (

                    activities.map((activity) => (

                        <div
                            key={activity.id}
                            className="border-l-4 border-blue-500 pl-4 py-2"
                        >

                            <p className="font-semibold">

                                {activity.action}

                            </p>

                            <p className="text-sm text-gray-600">

                                {activity.description}

                            </p>

                            <div className="flex justify-between mt-2 text-xs text-gray-500">

                                <span>

                                    {activity.user}

                                </span>

                                <span>

                                    {activity.created_at}

                                </span>

                            </div>

                        </div>

                    ))

                )}

            </div>

        </div>

    );

};

export default RecentActivities;