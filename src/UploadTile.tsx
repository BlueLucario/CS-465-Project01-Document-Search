import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { useState } from 'react';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import Alert from '@mui/material/Alert';
import IconButton from '@mui/material/IconButton';
import Collapse from '@mui/material/Collapse';
import CloseIcon from '@mui/icons-material/Close';


export default function UploadTile() {
    const [severity, setSeverity] = useState("success");
    const [helperText, setHelperText] = useState('')
    const [open, setOpen] = useState(false);

    function uploadFile(e: React.ChangeEvent<HTMLInputElement>) {
        if (e.target.files) {
            let fileData = new FormData();
            fileData.append("file", e.target.files[0]);
            fetch('/api/relevantDocuments', {method: 'POST', body: fileData})
            .then((res) => {
                if (!res.ok) {
                    let error = new Error(res.statusText);
                    error.response = res;
                    error.status = res.status;
                    throw error
                }
                setHelperText('File uploaded successfully!');
                setSeverity('success');
            })
            .catch(err => {
                setSeverity("error"); 
                err.response.text().then((data: string) => (data.trim() != '') 
                ? setHelperText(`Error: ${data}`) 
                : setHelperText(`${err}`));
            })
            .finally(() => {setOpen(true); e.target.value='';});
        }
    }

    return (
        <>
            <Button component="label" startIcon={<CloudUploadIcon />}>
                Upload file
                <TextField type="file" style={{ display: 'none' }} inputProps={{accept:".txt"}} onChange={uploadFile} />
            </Button>

            {/* Sticky header alert */}
            <div style={{ position: "absolute", top: 0, left: 0, right: 0, zIndex: 999 }}>
                <Collapse in={open}>
                    <Alert severity={severity} variant="outlined" action={
                        <IconButton size="small" onClick={() => setOpen(false)}>
                            <CloseIcon fontSize="inherit" />
                        </IconButton>
                    }>
                        {helperText}
                    </Alert>
                </Collapse>    
            </div>     
        </>
    );
}