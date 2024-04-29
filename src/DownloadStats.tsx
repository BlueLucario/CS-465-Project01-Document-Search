import Button from '@mui/material/Button';
import { useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  maxWidth: '80vw',
  maxHeight: '80vh',
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

export default function DownloadStats() {
    const [statistics, setStatistics] = useState({});
    const [open, setOpen] = useState(false);

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

    function showStatistics() {
		fetch(`/api/statistics`)
				.then(res => res.json())
				.then(data => setStatistics(data))
                .then(() => setOpen(true))
	}

    function downloadStatistics() {
        downloadFile(JSON.stringify(statistics, null, 2), "stats.json", "text/json");
    }

    
    return (
        <>
        <Button onClick={showStatistics}>Show statistics</Button>
        <Modal
            open={open}
            onClose={() => {setOpen(false)}}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
            <Box sx={style}>
            <Typography id="modal-modal-title" variant="h6" component="h2" align="center">
                Statistics
            </Typography>
            <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                <p><strong>Total number of distinct words:</strong> {statistics['Total number of distinct words']}</p>
                <p><strong>Total number of words encountered:</strong> {statistics['Total number of words encountered']}</p>
                <p><strong>Top 100th word:</strong> {statistics['Top 100th word'][0]} (frequency: {statistics['Top 100th word'][1]})</p>
                <p><strong>Top 500th word:</strong> {statistics['Top 500th word'][0]} (frequency: {statistics['Top 500th word'][1]})</p>
                <p><strong>Top 1000th word:</strong> {statistics['Top 1000th word'][0]} (frequency: {statistics['Top 1000th word'][1]})</p>
                <Button onClick={downloadStatistics}>Download full statistics</Button>
            </Typography>
            </Box>
        </Modal>
        </>
    );
}