import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { AlertColor } from '@mui/material';


export default function UploadIcon(props: { showSnackbar: (severity: AlertColor, message: string) => void; }) {

    function uploadFile(e: React.ChangeEvent<HTMLInputElement>) {
        if (e.target.files) {
            const fileData = new FormData();
            fileData.append("file", e.target.files[0]);
            fetch('/api/relevantDocuments', {method: 'POST', body: fileData})
            .then((res) => {
                if (!res.ok) {
                    const error = new Error(res.statusText);
                    console.log(error)
                    error.response = res;
                    error.status = res.status;
                    throw error
                }
                setHelperText('File uploaded successfully!');
                setSeverity('success');
            })
            .catch((err) => {
                err.response.text().then((data: string) => {
                    const message = (data.trim() != '') ? `Error: ${data}` : `${err}`;
                    const severity = "error";
                    props.showSnackbar(severity, message);
                })
            })
        }
    }

	return (
		<>
			<Button component="label" startIcon={<CloudUploadIcon />}>
				Upload file
				<TextField type="file" style={{ display: 'none' }} inputProps={{accept:".txt"}} onChange={uploadFile} />
			</Button>
		</>
	);
}
