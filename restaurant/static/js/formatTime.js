function formatTime(time) {
    const ampm = time < 12 ? 'AM' : 'PM';
    const t = time < 12 ? time : time > 12 ? time - 12 : time;
    const label = `${t} ${ampm}`;
    return label;
}