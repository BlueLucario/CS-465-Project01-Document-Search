import TextField from '@mui/material/TextField';
import { useState } from 'react';
import SendIcon from '@mui/icons-material/Send';
import Grid from '@mui/material/Grid';
import List from '@mui/material/List';
import { AlertColor, Box, ListItemButton, ListItemText, Modal, Typography } from '@mui/material';
import LoadingButton from '@mui/lab/LoadingButton';
import UploadIcon from './UploadIcon';

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
    overflow: 'auto',
    p: 4,
};


export default function QueryTile(props: { showSnackbar: (severity: AlertColor, message: string) => void; }) {
    const [relevantDocuments, setRelevantDocuments] = useState([]);
    const [query, setQuery] = useState('');
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const [documentContent, setDocumentContent] = useState("")

    function sendQuery() {
        setLoading(true);

        fetch(`/api/relevantDocuments/${query.toString().toLowerCase()}`)
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
                .then(data => setRelevantDocuments((data.length == 0) ? ['No documents found'] : data))
                .catch((err) => {
                    err.response.text().then((data: string) => {
                        const message = (data.trim() != '') ? `Error: ${data}` : `${err}`;
                        const severity = "error";
                        props.showSnackbar(severity, message);
                    })
                })
                .finally(() => setLoading(false));
    }

    function showDocumentContent(id: string) {
        fetch(`/api/documentContent/${id}`)
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
        .then(data => {setDocumentContent(data); setOpen(true)})
        .catch((err) => {
            err.response.text().then((data: string) => {
                const message = (data.trim() != '') ? `Error: ${data}` : `${err}`;
                const severity = "error";
                props.showSnackbar(severity, message);
            })
        })
    }

    return (
        <>
            <Grid container spacing={1} alignItems="center">
                <Grid item>
                    <TextField style={{width: 350}} id="search-query" label="Search query"
                            variant="outlined" onChange={(e)=>setQuery(e.target.value)} 
                            onKeyDown={(e) => {if (e.key == 'Enter') {sendQuery()}}}/>
                </Grid>
                <Grid item>
                    <LoadingButton id="send-query" onClick={sendQuery} loading={loading}
                            endIcon={<SendIcon/>} loadingPosition="end" variant="contained">
                        <span>Send</span>
                    </LoadingButton>
                </Grid>
                <Grid item>
                    <UploadIcon showSnackbar={props.showSnackbar} />
                </Grid>
            </Grid> 

            <p>Relevant documents:</p>
            <Box sx={{maxHeight: '300px', overflow: 'auto'}}>

                <span>{relevantDocuments.map(document => 
                    <List key={`list-${document}`}>
                        <ListItemButton key={`listItem-${document["name"]}`} onClick={() => showDocumentContent(document["id"])} /* Assumes document name is filepath*/>
                            <ListItemText key={`listItemText-${document["name"]}`} primary={document["name"]} />
                        </ListItemButton>
                    </List>
                )}</span>
            </Box>

            <Modal
                open={open}
                onClose={() => {setOpen(false)}}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                <Typography variant="h6" component="h2" align="center">
                    Document Content
                </Typography>
                <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                    <p>{documentContent}</p>
                </Typography>
                </Box>
            </Modal>
        </>
    );
}
