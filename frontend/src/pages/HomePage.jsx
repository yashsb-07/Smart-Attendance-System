import PageHeader from
"../components/common/PageHeader";

import StatsCard from
"../components/common/StatsCard";

import ContentCard from
"../components/common/ContentCard";

function HomePage() {

    return (

        <>

            <PageHeader
                title="Dashboard"
                subtitle="
                Welcome to Smart Attendance System
                "
            />

            <div className="row g-4">

                <div className="col-md-4">

                    <StatsCard
                        title="Students"
                        value="250"
                    />

                </div>

                <div className="col-md-4">

                    <StatsCard
                        title="Present"
                        value="220"
                    />

                </div>

                <div className="col-md-4">

                    <StatsCard
                        title="Absent"
                        value="30"
                    />

                </div>

            </div>

            <div className="mt-4">

                <ContentCard
                    title="
                    Recent Activity
                    "
                >

                    <p>
                        Dashboard
                        foundation ready.
                    </p>

                </ContentCard>

            </div>

        </>
    );
}

export default HomePage;