function UnauthorizedPage() {

    return (
        <div className="container mt-5">

            <div className="alert alert-danger">

                <h3>Access Denied</h3>

                <p>
                    You do not have permission
                    to access this page.
                </p>

            </div>

        </div>
    );
}

export default UnauthorizedPage;