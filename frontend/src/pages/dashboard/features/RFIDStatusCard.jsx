import React from "react";
import { Wifi, Tag, ScanLine } from "lucide-react";

const RFIDStatusCard = ({ rfid = {} }) => {
    return (
        <div className="bg-white rounded-xl shadow p-5">

            <div className="flex items-center justify-between mb-5">

                <h2 className="text-lg font-semibold">
                    RFID Status
                </h2>

                <Wifi className="text-blue-600" size={24} />

            </div>

            <div className="space-y-4">

                <div className="flex justify-between">

                    <div className="flex items-center gap-2">

                        <Tag size={18} />

                        <span>Registered Tags</span>

                    </div>

                    <span className="font-bold">
                        {rfid.registered_tags || 0}
                    </span>

                </div>

                <div className="flex justify-between">

                    <div className="flex items-center gap-2">

                        <ScanLine size={18} />

                        <span>Today's Scans</span>

                    </div>

                    <span className="font-bold">
                        {rfid.today_scans || 0}
                    </span>

                </div>

                <div className="flex justify-between">

                    <span>Reader Status</span>

                    <span
                        className={`font-semibold ${
                            rfid.reader_online
                                ? "text-green-600"
                                : "text-red-600"
                        }`}
                    >
                        {rfid.reader_online ? "Online" : "Offline"}
                    </span>

                </div>

                <div className="flex justify-between">

                    <span>Failed Scans</span>

                    <span className="font-bold text-red-600">
                        {rfid.failed_scans || 0}
                    </span>

                </div>

            </div>

        </div>
    );
};

export default RFIDStatusCard;