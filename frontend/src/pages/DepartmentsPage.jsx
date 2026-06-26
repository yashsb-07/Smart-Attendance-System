import {
    useEffect,
    useState,
} from "react";

import PageHeader from
"../components/common/PageHeader";

import ContentCard from
"../components/common/ContentCard";

import {
    getDepartments,
    createDepartment,
} from "../services/departmentService";

function DepartmentsPage() {

    const [departments,
        setDepartments] = useState([]);

    const [formData,
        setFormData] = useState({
            name: "",
            code: "",
            description: "",
        });

    const fetchDepartments =
        async () => {

            const data =
                await getDepartments();

            setDepartments(data);
        };

    useEffect(() => {

        fetchDepartments();

    }, []);

    const handleChange = (e) => {

        setFormData({
            ...formData,
            [e.target.name]:
                e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            console.log("Submitting:", formData);

            const response =
                await createDepartment(formData);

            console.log("Created:", response);

            setFormData({
                name: "",
                code: "",
                description: "",
            });

            fetchDepartments();

        } catch (error) {
            console.error(
                "Department create error:",
                error.response?.data || error
            );
        }
    };

    return (
        <>
            <PageHeader
                title="Departments"
                subtitle="
                Manage all departments
                "
            />

            <div className="row">

                <div className="col-md-4">

                    <ContentCard
                        title="
                        Add Department
                        "
                    >

                        <form
                            onSubmit={
                                handleSubmit
                            }
                        >

                            <input
                                type="text"
                                name="name"
                                className="
                                form-control
                                mb-3
                                "
                                placeholder="
                                Department Name
                                "
                                value={
                                    formData.name
                                }
                                onChange={
                                    handleChange
                                }
                                required
                            />

                            <input
                                type="text"
                                name="code"
                                className="
                                form-control
                                mb-3
                                "
                                placeholder="
                                Department Code
                                "
                                value={
                                    formData.code
                                }
                                onChange={
                                    handleChange
                                }
                                required
                            />

                            <textarea
                                name="description"
                                className="
                                form-control
                                mb-3
                                "
                                placeholder="
                                Description
                                "
                                value={
                                    formData.description
                                }
                                onChange={
                                    handleChange
                                }
                            />

                            <button
                                className="
                                btn
                                btn-primary
                                w-100
                                "
                            >
                                Add
                            </button>

                        </form>

                    </ContentCard>

                </div>

                <div className="col-md-8">

                    <ContentCard
                        title="
                        Department List
                        "
                    >

                        <table
                            className="
                            table
                            table-bordered
                            "
                        >

                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Code</th>
                                    <th>Description</th>
                                </tr>
                            </thead>

                            <tbody>

                                {departments.map(
                                    (
                                        dept
                                    ) => (
                                        <tr
                                            key={
                                                dept.id
                                            }
                                        >
                                            <td>
                                                {
                                                    dept.id
                                                }
                                            </td>
                                            <td>
                                                {
                                                    dept.name
                                                }
                                            </td>
                                            <td>
                                                {
                                                    dept.code
                                                }
                                            </td>
                                            <td>
                                                {
                                                    dept.description
                                                }
                                            </td>
                                        </tr>
                                    )
                                )}

                            </tbody>

                        </table>

                    </ContentCard>

                </div>

            </div>
        </>
    );
}

export default DepartmentsPage;