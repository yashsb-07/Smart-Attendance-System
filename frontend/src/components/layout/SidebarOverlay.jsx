function SidebarOverlay({

    show,
    onClick,

}) {

    if (!show) {

        return null;
    }

    return (

        <div
            onClick={onClick}
            style={{
                position: "fixed",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
                background:
                    "rgba(0,0,0,0.4)",
                zIndex: 999,
            }}
        />
    );
}

export default SidebarOverlay;