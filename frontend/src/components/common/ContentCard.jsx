function ContentCard({

    title,

    children,

}) {

    return (

        <div
            className="
                card
                shadow-sm
                border-0
            "
        >

            <div
                className="card-body"
            >

                <h5
                    className="mb-3"
                >
                    {title}
                </h5>

                {children}

            </div>

        </div>
    );
}

export default ContentCard;