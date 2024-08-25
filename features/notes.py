import datetime

class Notes:
    def __init__(self):
        self.notes = {}

    def add_note(self, user_id, content):
        if user_id not in self.notes:
            self.notes[user_id] = []
        
        timestamp = datetime.datetime.now()
        self.notes[user_id].append((timestamp, content))
        return f"Note added: {content}"

    def get_notes(self, user_id):
        if user_id not in self.notes or not self.notes[user_id]:
            return "You have no notes."
        
        note_list = [f"{n[0].strftime('%Y-%m-%d %H:%M')}: {n[1]}" for n in self.notes[user_id]]
        return "Your notes:\n" + "\n".join(note_list)

    def remove_note(self, user_id, index):
        if user_id not in self.notes or index >= len(self.notes[user_id]):
            return "Invalid note index."
        
        removed_note = self.notes[user_id].pop(index)
        return f"Removed note: {removed_note[1]}"

    def search_notes(self, user_id, keyword):
        if user_id not in self.notes:
            return "You have no notes."
        
        matching_notes = [n for n in self.notes[user_id] if keyword.lower() in n[1].lower()]
        if not matching_notes:
            return f"No notes found containing '{keyword}'."
        
        note_list = [f"{n[0].strftime('%Y-%m-%d %H:%M')}: {n[1]}" for n in matching_notes]
        return f"Notes containing '{keyword}':\n" + "\n".join(note_list)