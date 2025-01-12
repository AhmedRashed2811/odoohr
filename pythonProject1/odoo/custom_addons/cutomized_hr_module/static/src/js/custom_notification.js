/** @odoo-module **/

import { registry } from "@web/core/registry";

const { Component } = owl;
const NotificationService = registry.category("services").get("notification");

class SimpleNotificationHandler extends Component {
    constructor() {
        super(...arguments);
        const busService = this.env.services.bus_service;

        // Listen to the 'simple_notification' channel
        busService.addChannel("simple_notification");
        busService.on("notification", this, this._onNotification);
    }

    _onNotification({ type, payload }) {
        if (type === "simple_notification") {
            const { title, message, type, sticky } = payload;

            // Trigger Odoo Notification
            this.env.services.notification.add(
                message,
                { title, type: type || "info", sticky: sticky || false }
            );
        }
    }
}

registry.category("services").add("simple_notification_handler", SimpleNotificationHandler);
