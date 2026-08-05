import React from "react";

const AlertsCard = ({ alerts = [] }) => {

    return (

        <div className="bg-white rounded-xl shadow p-5">

            <h2 className="text-lg font-semibold text-red-600 mb-5">
                System Alerts
            </h2>

            <div className="space-y-3">

                {alerts.length === 0 ? (

                    <p className="text-gray-500">
                        No active alerts.
                    </p>

                ) : (

                    alerts.map((alert) => (

                        <div
                            key={alert.id}
                            className="border rounded-lg p-3 hover:bg-gray-50"
                        >

                            <div className="flex justify-between">

                                <span className="font-semibold">

                                    {alert.medicine_name}

                                </span>

                                <span className="text-red-600">

                                    {alert.alert_type}

                                </span>

                            </div>

                            <p className="text-sm text-gray-600 mt-2">

                                {alert.message}

                            </p>

                        </div>

                    ))

                )}

            </div>

        </div>

    );

};

export default AlertsCard;