// DownloadStats.tsx (typescriptreact)
// Will Moss & Benjamin Weeg (Group 1)
// Started: 
// Last edited: 2024-05-09 (yyyy mm dd)

import Button from '@mui/material/Button';
import { useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import { AlertColor } from '@mui/material';

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

interface StatSummary {
    "Total number of distinct words": number;
    "Total number of words encountered": number;
    "Top 100th word": [string, number];
    "Top 500th word": [string, number];
    "Top 1000th word": [string, number];
}

const defaultStatSummary: StatSummary = {
    "Total number of distinct words": -1,
    "Total number of words encountered": -1,
    "Top 100th word": ["N/A", -1],
    "Top 500th word": ["N/A", -1],
    "Top 1000th word": ["N/A", -1],
}

export default function DownloadStats(props: { showSnackbar: (severity: AlertColor, message: string) => void; }) {
    const [statistics, setStatistics] = useState({});
    const [statSummary, setStatSummary] = useState<StatSummary>(defaultStatSummary);
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
                .then(res => {
                    if (!res.ok) {
                        const error = new Error(res.statusText);
                        console.log(error);
                        error.response = res;
                        error.status = res.status;
                        throw error;
                    }
                    return res.json()
                })
                .then(data => {setStatistics(data); setStatSummary(data);})
                .then(() => setOpen(true))
                .catch((err) => {
                    err.response.text().then((data: string) => {
                        const message = (data.trim() != '') ? `Error: ${data}` : `${err}`;
                        const severity = "error";
                        props.showSnackbar(severity, message);
                    })
                })
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
                <p><strong>Total number of distinct words:</strong> {statSummary['Total number of distinct words']}</p>
                <p><strong>Total number of words encountered:</strong> {statSummary['Total number of words encountered']}</p>
                <p><strong>Top 100th word:</strong> {statSummary['Top 100th word'][0]} (frequency: {statSummary['Top 100th word'][1]})</p>
                <p><strong>Top 500th word:</strong> {statSummary['Top 500th word'][0]} (frequency: {statSummary['Top 500th word'][1]})</p>
                <p><strong>Top 1000th word:</strong> {statSummary['Top 1000th word'][0]} (frequency: {statSummary['Top 1000th word'][1]})</p>
                <Button onClick={downloadStatistics}>Download full statistics</Button>
            </Typography>
            </Box>
        </Modal>
        </>
    );
}
