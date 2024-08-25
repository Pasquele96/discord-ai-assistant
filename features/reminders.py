import datetime
import asyncio

class Reminders:
    def __init__(self):
        self.reminders = {}

    def add_reminder(self, user_id, time, reminder):
        try:
            reminder_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
            if reminder_time <= datetime.datetime.now():
                return "Please provide a future time for the reminder."
            
            if user_id not in self.reminders:
                self.reminders[user_id] = []
            
            self.reminders[user_id].append((reminder_time, reminder))
            asyncio.create_task(self._send_reminder(user_id, reminder_time, reminder))
            return f"Reminder set for {time}: {reminder}"
        except ValueError:
            return "Invalid time format. Please use YYYY-MM-DD HH:MM."

    async def _send_reminder(self, user_id, reminder_time, reminder):
        await asyncio.sleep((reminder_time - datetime.datetime.now()).total_seconds())
        # In a real implementation, you would send a message to the user here
        print(f"Reminder for user {user_id}: {reminder}")
        self.reminders[user_id].remove((reminder_time, reminder))

    def get_reminders(self, user_id):
        if user_id not in self.reminders or not self.reminders[user_id]:
            return "You have no reminders set."
        
        reminder_list = [f"{r[0].strftime('%Y-%m-%d %H:%M')}: {r[1]}" for r in self.reminders[user_id]]
        return "Your reminders:\n" + "\n".join(reminder_list)

    def remove_reminder(self, user_id, index):
        if user_id not in self.reminders or index >= len(self.reminders[user_id]):
            return "Invalid reminder index."
        
        removed_reminder = self.reminders[user_id].pop(index)
        return f"Removed reminder: {removed_reminder[0].strftime('%Y-%m-%d %H:%M')}: {removed_reminder[1]}"