// App.tsx (typescriptreact)
// Will Moss & Benjamin Weeg (Group 1)
// Started: 
// Last edited: 2024-05-09 (yyyy mm dd)

import './App.css'
import './QueryTile'
import QueryTile from './QueryTile'
import Grid from '@mui/material/Grid';
import DownloadStats from './DownloadStats';
import SharedSnackbar from './SharedSnackbar';
import { useState } from 'react';
import { AlertColor } from '@mui/material';

export default function App() {
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarSeverity, setSnackbarSeverity] = useState<AlertColor>("info");
    const [snackbarMessage, setSnackbarMessage] = useState("");

    function showSnackbar(severity: AlertColor, message: string) {
        setSnackbarOpen(false);
        setTimeout(() => {
            setSnackbarSeverity(severity);
            setSnackbarMessage(message);
            setSnackbarOpen(true);
        }, 100);
    }

    return (
        <>
            <Grid container direction="column" spacing={2}>
                <Grid item>
                    <h1>Document Retrieval</h1>
                </Grid>
                <Grid item>
                    <QueryTile showSnackbar={showSnackbar} />
                </Grid>
            </Grid>

            <div style={{ position: "absolute", bottom: 10, right: 10, zIndex: 999 }}>
                <DownloadStats showSnackbar={showSnackbar} />
            </div>

            <SharedSnackbar open={snackbarOpen}
                    handleClose={() => setSnackbarOpen(false)}
                    severity={snackbarSeverity}
                    message={snackbarMessage} />
        </>
    )
}
