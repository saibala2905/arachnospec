export default function YoutubeInput() {
    const [youtubeUrl, setYoutubeUrl] = useState('');
    const [loading, setLoading] = useState(false);

    const handleUrlSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            const response = await fetch('http://localhost:5000/process_video', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: youtubeUrl })
            });
            const data = await response.json();
            onVideoProcessed(data);  // Pass video details up to the parent component
            setYoutubeUrl('');  // Clear the input field after submitting
        } catch (error) {
            console.error('Failed to process video:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleUrlSubmit} className="p-4">
            <input
                type="text"
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
                placeholder="Enter YouTube URL here..."
                className="border p-2 rounded w-full"
                disabled={loading}
            />
            <button type="submit" className="mt-2 bg-blue-500 text-white p-2 rounded" disabled={loading}>
                {loading ? "Processing..." : "Process Video"}
            </button>
        </form>
    );
}