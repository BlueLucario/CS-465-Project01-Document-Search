import Button from '@mui/material/Button';

export default function DownloadStats() {
    const downloadFile = (data: string, fileName: string, fileType: string) => {
        // Create a blob with the data we want to download as a file
        const blob = new Blob([data], { type: fileType })
        // Create an anchor element and dispatch a click event on it
        // to trigger a download
        const a = document.createElement('a')
        a.download = fileName
        a.href = window.URL.createObjectURL(blob)
        const clickEvt = new MouseEvent('click', {
            view: window,
            bubbles: true,
            cancelable: true,
        })
        a.dispatchEvent(clickEvt)
        a.remove()
    }

    function exportStatistics() {
		fetch(`/api/statistics`)
				.then(res => res.json())
				.then(data => {downloadFile(JSON.stringify(data), "stats.json", "text/json")})
	}

    
    return (
        <>
        <Button onClick={exportStatistics}>Download statistics</Button>
        </>
    );
}