type Props = {
  children: React.ReactNode;
};

export default function Container({ children }: Props) {
  return <div className="px-4 mx-auto h-[95vh]">{children}</div>;
}
