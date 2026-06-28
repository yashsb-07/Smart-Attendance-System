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
    updateDepartment,
    deleteDepartment,
} from "../services/departmentService";

function DepartmentsPage() {

    const [departments,
        setDepartments] = useState([]);

    const [search,
        setSearch] = useState("");

    const [editingId,
        setEditingId] = useState(null);

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

            if (editingId) {

                await updateDepartment(
                    editingId,
                    formData
                );

                setEditingId(null);

            } else {

                await createDepartment(
                    formData
                );
            }

            setFormData({
                name: "",
                code: "",
                description: "",
            });

            fetchDepartments();

        } catch (error) {

            console.error(
                "Department error:",
                error.response?.data || error
            );
        }
    };

    const handleEdit = (dept) => {

        setEditingId(dept.id);

        setFormData({
            name: dept.name,
            code: dept.code,
            description:
                dept.description || "",
        });
    };

    const handleDelete = async (id) => {

        try {

            await deleteDepartment(id);

            fetchDepartments();

        } catch (error) {

            console.error(
                "Delete error:",
                error.response?.data || error
            );
        }
    };

    const filteredDepartments =
        departments.filter((dept) =>
            dept.name
                .toLowerCase()
                .includes(
                    search.toLowerCase()
                )
        );

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
                                {editingId
                                    ? "Update Department"
                                    : "Add Department"}
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

                        <input
                            type="text"
                            className="
                            form-control
                            mb-3
                            "
                            placeholder="
                            Search department...
                            "
                            value={search}
                            onChange={(e) =>
                                setSearch(
                                    e.target.value
                                )
                            }
                        />

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
                                    <th>Actions</th>
                                </tr>
                            </thead>

                            <tbody>

                                {filteredDepartments.map(
                                    (dept) => (
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

                                            <td>

                                                <button
                                                    className="
                                                    btn
                                                    btn-warning
                                                    btn-sm
                                                    me-2
                                                    "
                                                    onClick={() =>
                                                        handleEdit(
                                                            dept
                                                        )
                                                    }
                                                >
                                                    Edit
                                                </button>

                                                <button
                                                    className="
                                                    btn
                                                    btn-danger
                                                    btn-sm
                                                    "
                                                    onClick={() =>
                                                        handleDelete(
                                                            dept.id
                                                        )
                                                    }
                                                >
                                                    Delete
                                                </button>

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