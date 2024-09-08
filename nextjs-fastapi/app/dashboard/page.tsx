import { Plus, Upload, BarChart2, Bell } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface Class {
  id: number;
  name: string;
  code: string;
  students: number;
}

interface Activity {
  id: number;
  action: string;
  class: string;
  date: string;
}

interface Notification {
  id: number;
  message: string;
  time: string;
}

const ProfessorDashboard = () => {
  const classes: Class[] = [
    { id: 1, name: 'Introduction to Computer Science', code: 'CS101', students: 120 },
    { id: 2, name: 'Data Structures', code: 'CS201', students: 80 },
    { id: 3, name: 'Algorithms', code: 'CS301', students: 60 },
  ];

  const recentActivity: Activity[] = [
    { id: 1, action: 'Test Uploaded', class: 'CS101', date: '2024-09-07' },
    { id: 2, action: 'Grading Completed', class: 'CS201', date: '2024-09-06' },
    { id: 3, action: 'New Class Added', class: 'CS301', date: '2024-09-05' },
  ];

  const notifications: Notification[] = [
    { id: 1, message: 'New submissions for CS101 midterm', time: '2 hours ago' },
    { id: 2, message: 'Grading completed for CS201 assignment', time: '1 day ago' },
  ];

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-8 text-gray-900">Professor Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
        <Card>
          <CardHeader>
            <CardTitle className="text-xl font-semibold">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col space-y-4">
            <Button variant="outline"><Plus className="mr-2 h-4 w-4" /> Add New Class</Button>
            <Button variant="outline"><Upload className="mr-2 h-4 w-4" /> Upload Test</Button>
            <Button variant="outline"><BarChart2 className="mr-2 h-4 w-4" /> View Reports</Button>
          </CardContent>
        </Card>

        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="text-xl font-semibold">Classes Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Class Name</TableHead>
                  <TableHead>Code</TableHead>
                  <TableHead>Students</TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {classes.map((cls) => (
                  <TableRow key={cls.id}>
                    <TableCell>{cls.name}</TableCell>
                    <TableCell>{cls.code}</TableCell>
                    <TableCell>{cls.students}</TableCell>
                    <TableCell>
                      <Button variant="link">View</Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle className="text-xl font-semibold">Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-4">
              {recentActivity.map((activity) => (
                <li key={activity.id} className="flex justify-between items-center">
                  <span>{activity.action} - {activity.class}</span>
                  <span className="text-sm text-gray-500">{activity.date}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Bell className="mr-2 h-5 w-5" />
              <span className="text-xl font-semibold">Notifications</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-4">
              {notifications.map((notification) => (
                <li key={notification.id} className="flex justify-between items-center">
                  <span>{notification.message}</span>
                  <span className="text-sm text-gray-500">{notification.time}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
export default ProfessorDashboard;