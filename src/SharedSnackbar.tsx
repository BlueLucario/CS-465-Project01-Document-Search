// SharedSnackbar.tsx (typescriptreact)
// Will Moss & Benjamin Weeg (Group 1)
// Started: 
// Last edited: 2024-05-09 (yyyy mm dd)

import { Alert, AlertColor, Snackbar } from "@mui/material";

export default function SharedSnackbar(props: SharedSnackbarProps) {
    return (
        <>
            <Snackbar open={props.open} autoHideDuration={5000} onClose={props.handleClose}>
                <Alert
                    onClose={props.handleClose}
                    severity={props.severity}
                    variant="filled"
                    sx={{ width: '100%' }}
                >
                    {props.message}
                </Alert>
            </Snackbar>
        </>
    )
}

export interface SharedSnackbarProps {
    open: boolean;
    severity: AlertColor;
    message: string;
    handleClose: () => void;
}

